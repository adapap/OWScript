import * as vscode from 'vscode';
const fs = require('fs');
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
			fs.access(config.path, async (err: any) => {
				// Open error dialog if directory doesn't exist
				if (err) {
					let open = await vscode.window.showErrorMessage('Could not locate OWScript path.', 'Open Settings');
					if (open == 'Open Settings') {
						await vscode.commands.executeCommand('workbench.action.openSettings');
					}
				}
				// Otherwise, run a shell command to compile the source
				else {
					console.log('Compiling source...');
					exec(command, async (error: string, stdout: string, stderr: string) => {
						if (error) {
							console.warn(error);
						}
						await setOutput(stdout);
					});
				}
			});
			async function setOutput(str: string) {
				OWScriptDocument.output = str;
				console.log('Opening output document...');
				// Open the text document with the resulting compiled code
				let uri = vscode.Uri.parse("owscript:" + "Workshop Code");
				let doc = await vscode.workspace.openTextDocument(uri);
				await vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
			}
		})
	);
}

export function deactivate() {}

class OWScriptDocument implements vscode.TextDocumentContentProvider {
	public static output: string;
	provideTextDocumentContent(uri: vscode.Uri): string {
		return OWScriptDocument.output;
	}
}