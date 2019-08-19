"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const vscode = require("vscode");
const fs = require("fs");
const fileSystem_1 = require("./fileSystem");
const { copy } = require('copy-paste');
const { basename } = require('path');
const { exec } = require('child_process');
function activate(context) {
    // tslint:disable-next-line: semicolon
    console.log('OWScript extension activated.');
    const config = vscode.workspace.getConfiguration('owscript');
    const channel = vscode.window.createOutputChannel('OWScript');
    let owfs = new fileSystem_1.OWScriptFS();
    context.subscriptions.push(vscode.workspace.registerFileSystemProvider('owfs', owfs, { isCaseSensitive: true }));
    context.subscriptions.push(vscode.commands.registerTextEditorCommand('owscript.compile', (editor) => __awaiter(this, void 0, void 0, function* () {
        channel.clear();
        const path = editor.document.uri.fsPath;
        const command = `set PYTHONIOENCODING=utf-8&python OWScript.py "${path}"`;
        // Check if the OWScript directory exists using fs.access
        function pathExists(path) {
            return new Promise((res, rej) => {
                fs.access(path, (err) => __awaiter(this, void 0, void 0, function* () {
                    err ? res(false) : res(true);
                }));
            });
        }
        // Compile the source into workshop code
        function compileSource(command) {
            return new Promise((res, rej) => {
                exec(command, {
                    cwd: config.path
                }, (err, stdout, stderr) => __awaiter(this, void 0, void 0, function* () {
                    res({ stdout: stdout, stderr: stderr });
                }));
            });
        }
        if (yield pathExists(config.path)) {
            let result = yield compileSource(command);
            if (result.stderr) {
                let infoMessages = [];
                let warningMessages = [];
                let errorMessages = [];
                for (let rawMsg of result.stderr.split('\n')) {
                    // tslint:disable-next-line: semicolon
                    let msg = rawMsg.replace(/^\[[A-Z]*?\]\s*/g, '');
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
                let doc = yield vscode.workspace.openTextDocument(uri);
                vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
                // Copy output
                if (config.clipboard == true) {
                    copy(result.stdout, () => { });
                    vscode.window.showInformationMessage('Code copied to clipboard.');
                }
            }
        }
        else {
            let open = yield vscode.window.showErrorMessage('Could not locate OWScript path.', 'Open Settings');
            if (open == 'Open Settings') {
                yield vscode.commands.executeCommand('workbench.action.openSettings');
            }
        }
    })));
    vscode.workspace.onDidSaveTextDocument((doc) => __awaiter(this, void 0, void 0, function* () {
        if (doc.languageId == 'owscript' && !doc.isUntitled && config.compileOnSave == true) {
            yield vscode.commands.executeCommand('owscript.compile');
        }
    }));
}
exports.activate = activate;
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map