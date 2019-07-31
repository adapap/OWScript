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
const fs = require('fs');
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
        fs.access(config.path, (err) => __awaiter(this, void 0, void 0, function* () {
            // Open error dialog if directory doesn't exist
            if (err) {
                let open = yield vscode.window.showErrorMessage('Could not locate OWScript path.', 'Open Settings');
                if (open == 'Open Settings') {
                    yield vscode.commands.executeCommand('workbench.action.openSettings');
                }
            }
            // Otherwise, run a shell command to compile the source
            else {
                console.log('Compiling source...');
                exec(command, (error, stdout, stderr) => __awaiter(this, void 0, void 0, function* () {
                    if (error) {
                        console.warn(error);
                    }
                    yield setOutput(stdout);
                }));
            }
        }));
        function setOutput(str) {
            return __awaiter(this, void 0, void 0, function* () {
                OWScriptDocument.output = str;
                console.log('Opening output document...');
                // Open the text document with the resulting compiled code
                let uri = vscode.Uri.parse("owscript:" + "Workshop Code");
                let doc = yield vscode.workspace.openTextDocument(uri);
                yield vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
            });
        }
    })));
}
exports.activate = activate;
function deactivate() { }
exports.deactivate = deactivate;
class OWScriptDocument {
    provideTextDocumentContent(uri) {
        return OWScriptDocument.output;
    }
}
//# sourceMappingURL=extension.js.map