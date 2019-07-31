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
const basename = require('path').basename;
const exec = require('child_process').exec;
function activate(context) {
    console.log('OWScript extension activated.');
    const scheme = 'owscript';
    const document = new OWScriptDocument();
    context.subscriptions.push(vscode.workspace.registerTextDocumentContentProvider(scheme, document));
    context.subscriptions.push(vscode.commands.registerTextEditorCommand('owscript.compile', (editor) => __awaiter(this, void 0, void 0, function* () {
        const path = editor.document.uri.fsPath;
        const config = vscode.workspace.getConfiguration('owscript');
        const command = `cd ${config.path} & cat ${path} | python OWScript.py`;
        // Check if the OWScript directory exists using fs.access
        function pathExists(path) {
            return new Promise((res, rej) => {
                fs.access(path, (err) => __awaiter(this, void 0, void 0, function* () {
                    err ? res(false) : res(true);
                }));
            });
        }
        function compileSource(command) {
            return new Promise((res, rej) => {
                exec(command, (err, stdout, stderr) => __awaiter(this, void 0, void 0, function* () {
                    err ? rej(err) : res({ stdout: stdout, stderr: stderr });
                }));
            });
        }
        if (yield pathExists(config.path)) {
            let result = yield compileSource(command);
            OWScriptDocument.output = result.stdout;
            if (result.stderr) {
                yield vscode.window.showErrorMessage(result.stderr);
            }
            // Open the text document with the resulting compiled code
            let uri = vscode.Uri.parse('owscript:' + basename(path) + ' - Workshop Code');
            let doc = yield vscode.workspace.openTextDocument(uri);
            yield vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
        }
        else {
            let open = yield vscode.window.showErrorMessage('Could not locate OWScript path.', 'Open Settings');
            if (open == 'Open Settings') {
                yield vscode.commands.executeCommand('workbench.action.openSettings');
            }
        }
    })));
}
exports.activate = activate;
function deactivate() { }
exports.deactivate = deactivate;
class OWScriptDocument {
    constructor() {
        this.onDidChangeEmitter = new vscode.EventEmitter();
        this.onDidChange = this.onDidChangeEmitter.event;
    }
    provideTextDocumentContent(uri) {
        return OWScriptDocument.output;
    }
}
//# sourceMappingURL=extension.js.map