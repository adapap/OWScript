import * as vscode from 'vscode';
import fs = require('fs');
const { copy } = require('copy-paste');
const { basename } = require('path');
const { exec } = require('child_process');

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
					let infoMessages = [];
					let warningMessages = [];
					let errorMessages = [];
					for (let rawMsg of result.stderr.split('\n')) {
						let msg = rawMsg.replace(/^\[[A-Z]*?\]\s*/g, '')
						if (rawMsg.startsWith("[INFO]")) {
							infoMessages.push(msg);
						}
						else if (rawMsg.startsWith("[WARNING]") || rawMsg.startsWith("[DEBUG]")) {
							warningMessages.push(msg);
						}
						else {
							errorMessages.push(msg);
						}
					}
					if (infoMessages.length > 0) {
						vscode.window.showInformationMessage(infoMessages.join('\n'));
					}
					if (warningMessages.length > 0) {
						vscode.window.showWarningMessage(warningMessages.join('\n'));
					}
					if (errorMessages.length > 0) {
						vscode.window.showErrorMessage('Error while compiling ' + path + ' (see debug console)');
						console.error(errorMessages.join('\n'));
						// Focus error automatically?
					}
				}
				if (result.stdout != '') {
					// Open the text document with the resulting compiled code
					let uri = vscode.Uri.parse('owscript:' + basename(path) + ' - Workshop Code');
					let doc = await vscode.workspace.openTextDocument(uri);
					vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
					// Copy output
					if (config.clipboard == true) {
						copy(OWScriptDocument.output, () => {});
						vscode.window.showInformationMessage('Code copied to clipboard.');
					}
				}
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