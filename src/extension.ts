import * as vscode from 'vscode';
import fs = require('fs');
import { OWScriptFS } from './fileSystem';
const { copy } = require('copy-paste');
const { basename } = require('path');
const { exec } = require('child_process');

export function activate(context: vscode.ExtensionContext) {
    console.log('OWScript extension activated.')
    const config = vscode.workspace.getConfiguration('owscript');
    const channel = vscode.window.createOutputChannel('OWScript');
    let owfs = new OWScriptFS();
    context.subscriptions.push(vscode.workspace.registerFileSystemProvider('owfs', owfs, { isCaseSensitive: true }));

    context.subscriptions.push(
        vscode.commands.registerTextEditorCommand('owscript.compile', async (editor) => {
            channel.clear()
            const path = editor.document.uri.fsPath;
            const command = `set PYTHONIOENCODING=utf-8&cat "${path}" | python OWScript.py`;
            // Check if the OWScript directory exists using fs.access
            function pathExists(path: string) {
                return new Promise((res, rej) => {
                    fs.access(path, async (err: any) => {
                        err ? res(false) : res(true);
                    })
                })
            }

            // Compile the source into workshop code
            function compileSource(command: string) {
                return new Promise((res, rej) => {
                    exec(command,
                    {
                        cwd: config.path
                    },
                    async (err: string, stdout: string, stderr: string) => {
                        res({stdout: stdout, stderr: stderr});
                    })
                })
            }

            if (await pathExists(config.path)) {
                let result: any = await compileSource(command);
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
                        vscode.window.showErrorMessage('Error while compiling ' + basename(path));
                        channel.append(errorMessages.join('\n'));
                        channel.show();
                        // Focus error automatically?
                    }
                }
                if (result.stdout != '') {
                    // Open the text document with the resulting compiled code
                    let code = Buffer.from(result.stdout);
                    let uri = vscode.Uri.parse('owfs:/' + basename(path) + ' - Workshop Code');
                    owfs.writeFile(uri, code, { create: true, overwrite: true });
                    let doc = await vscode.workspace.openTextDocument(uri);
                    vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
                    // Copy output
                    if (config.clipboard == true) {
                        copy(result.stdout, () => {});
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

    vscode.workspace.onDidSaveTextDocument(async doc => {
        if (doc.languageId == 'owscript' && !doc.isUntitled && config.compileOnSave == true) {
            await vscode.commands.executeCommand('owscript.compile');
        }
    })
}

export function deactivate() {}