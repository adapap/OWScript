import * as vscode from 'vscode';
import fs = require('fs');
const basename = require('path').basename;
const exec = require('child_process').exec;

export function activate(context: vscode.ExtensionContext) {
	console.log('OWScript extension activated.')

	const scheme = 'owscript';
	const document = new OWScriptDocument();
	context.subscriptions.push(vscode.workspace.registerTextDocumentContentProvider(scheme, document));

	context.subscriptions.push(
		vscode.commands.registerTextEditorCommand('owscript.compile', async (editor) => {
			const path = editor.document.uri.fsPath;
			const config = vscode.workspace.getConfiguration('owscript');
			const command = `cd ${config.path} & cat ${path} | python OWScript.py`;
			// Check if the OWScript directory exists using fs.access
			function pathExists(path: string) {
				return new Promise((res, rej) => {
					fs.access(path, async (err: any) => {
						err ? res(false) : res(true);
					})
				})
			}
			function compileSource(command: string) {
				return new Promise((res, rej) => {
					exec(command, async (err: string, stdout: string, stderr: string) => {
						err ? rej(err) : res({stdout: stdout, stderr: stderr});
					})
				})
			}
			if (await pathExists(config.path)) {
				let result: any = await compileSource(command);
				OWScriptDocument.output = result.stdout;
				if (result.stderr) {
					await vscode.window.showErrorMessage(result.stderr);
				}
				// Open the text document with the resulting compiled code
				let uri = vscode.Uri.parse('owscript:' + basename(path) + ' - Workshop Code');
				let doc = await vscode.workspace.openTextDocument(uri);
				await vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
			}
			else {
				let open = await vscode.window.showErrorMessage('Could not locate OWScript path.', 'Open Settings');
				if (open == 'Open Settings') {
					await vscode.commands.executeCommand('workbench.action.openSettings');
				}
			}
		})
	);
}

export function deactivate() {}

class OWScriptDocument implements vscode.TextDocumentContentProvider {
	public static output: string;

	onDidChangeEmitter = new vscode.EventEmitter<vscode.Uri>();
	onDidChange = this.onDidChangeEmitter.event;

	provideTextDocumentContent(uri: vscode.Uri): string {
		return OWScriptDocument.output;
	}
}