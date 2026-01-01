const vscode = require('vscode');
const path = require('path');
const fs = require('fs');

/**
 * Enhanced Path Parser (v3)
 * Handles hyphens, nested objects, and bracket counting.
 */
function getPathContent(text, targetPath) {
    const escapedPath = targetPath.replace(/\//g, '\\s*\\/\\s*');
    const startRegex = new RegExp(`@${escapedPath}\\s*\\(`, 'g');
    let match;
    const result = {};

    while ((match = startRegex.exec(text)) !== null) {
        let bracketCount = 1;
        let index = startRegex.lastIndex;
        let content = "";

        while (index < text.length && bracketCount > 0) {
            const char = text[index];
            if (char === '(') bracketCount++;
            else if (char === ')') bracketCount--;
            if (bracketCount > 0) content += char;
            index++;
        }

        const lines = content.split('\n');
        let currentObject = null;
        let objectName = null;

        lines.forEach(line => {
            const trimmed = line.trim();
            if (!trimmed || trimmed.startsWith('!') || trimmed === '(') return;

            if (trimmed === ')' && currentObject) {
                result[objectName] = currentObject;
                currentObject = null;
                objectName = null;
                return;
            }

            // Key regex supports hyphens [\w-]+
            const kvMatch = trimmed.match(/^([\w-]+):\s*(?:object:)?\s*(?:\(?\s*)?([^]*)$/);
            if (kvMatch) {
                const key = kvMatch[1];
                let val = kvMatch[2].trim().replace(/^\(|\)$/g, '').trim();
                
                if (val.startsWith('"') && val.endsWith('"')) val = val.substring(1, val.length - 1);
                if (val === 'true') val = true;
                if (val === 'false') val = false;

                if (line.includes('object: (')) {
                    objectName = key;
                    currentObject = {};
                } else if (currentObject) {
                    currentObject[key] = val;
                } else {
                    result[key] = val;
                }
            }
        });
    }
    return Object.keys(result).length > 0 ? result : null;
}

/**
 * Navigation Logic
 */
function findLocation(document, target, mode) {
    const text = document.getText();
    const lines = text.split('\n');
    
    if (mode === 'toDefinition') {
        if (target === '@root') return new vscode.Location(document.uri, new vscode.Position(0, 0));
        let searchRegex;
        if (target.startsWith('@')) {
            const cleanPath = target.substring(1).replace(/\//g, '\\/');
            searchRegex = new RegExp(`^\\s*@${cleanPath}\\s*(\\s|[\\(\\[\\{])`);
        } else if (target.startsWith('#')) {
            searchRegex = new RegExp(`^\\s*@templates\\s+${target.substring(1)}\\b`);
        }
        for (let i = 0; i < lines.length; i++) {
            if (searchRegex && searchRegex.test(lines[i])) {
                return new vscode.Location(document.uri, new vscode.Position(i, lines[i].indexOf('@') !== -1 ? lines[i].indexOf('@') : 0));
            }
        }
    } else {
        const symbol = target.replace('@templates ', '#').replace('@', '');
        const regex = new RegExp(`(?<!@templates\\s+)${symbol}\\b`, 'g');
        const match = regex.exec(text);
        if (match) return new vscode.Location(document.uri, document.positionAt(match.index));
    }
    return null;
}

function slugify(text) {
    return text.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '');
}

function activate(context) {
    const definitionsPath = path.join(context.extensionPath, 'panel/definitions.flon');

    // 1. VIRTUAL DOCUMENT PROVIDER
    const readOnlyProvider = new class {
        provideTextDocumentContent(uri) {
            const filePath = path.join(context.extensionPath, uri.path);
            return fs.readFileSync(filePath, 'utf8');
        }
    };
    context.subscriptions.push(vscode.workspace.registerTextDocumentContentProvider('flexion-sample', readOnlyProvider));

    // 2. DYNAMIC SIDEBAR
    class FlexionItem extends vscode.TreeItem {
        constructor(label, collapsibleState, command, icon, contextValue) {
            super(label, collapsibleState);
            this.command = command;
            this.iconPath = icon ? new vscode.ThemeIcon(icon) : null;
            this.contextValue = contextValue;
        }
    }

    const helpProvider = {
        getTreeItem: (item) => item,
        getChildren: async (element) => {
            if (!fs.existsSync(definitionsPath)) return [];
            const defText = fs.readFileSync(definitionsPath, 'utf8');

            if (element && element.isMarkdownFile) {
                const fullPath = path.join(context.extensionPath, 'panel', element.relPath);
                if (!fs.existsSync(fullPath)) return [];
                const content = fs.readFileSync(fullPath, 'utf8');
                
                // Return only section headers as children (No "Top" item)
                return content.split('\n')
                    .map(l => l.trim())
                    .filter(l => l.startsWith('## '))
                    .map(l => {
                        const title = l.replace('## ', '').trim();
                        return new FlexionItem(title, vscode.TreeItemCollapsibleState.None, {
                            command: 'flexion.jumpToWikiSection',
                            arguments: [element.relPath, slugify(title)]
                        }, 'symbol-method');
                    });
            }

            const pathInDef = element ? `root/panels/${element.contextValue}` : 'root/panels';
            const config = getPathContent(defText, pathInDef);
            if (!config) return [];

            if (!element) {
                return Object.entries(config).map(([key, name]) => 
                    new FlexionItem(name, vscode.TreeItemCollapsibleState.Collapsed, null, key === 'docs' ? 'book' : 'code', key)
                );
            }

            const fileType = config.file_type || "";
            const items = [];

            for (const [key, details] of Object.entries(config)) {
                if (key === 'file_type') continue;

                const displayName = (typeof details === 'object') ? (details.name || key) : details;
                const internalPath = `${element.contextValue}/${key}`;

                if (details.folder === true) {
                    items.push(new FlexionItem(displayName, vscode.TreeItemCollapsibleState.Collapsed, null, 'folder', internalPath));
                } else if (typeof details === 'object') {
                    const fileName = `${key}${fileType}`;
                    const relFilePath = path.join(element.contextValue, fileName);
                    const isMD = fileType === '.md';
                    
                    const item = new FlexionItem(
                        displayName, 
                        (isMD && details.jump === true) ? vscode.TreeItemCollapsibleState.Collapsed : vscode.TreeItemCollapsibleState.None,
                        {
                            command: isMD ? 'flexion.openWiki' : 'flexion.openExample',
                            arguments: [relFilePath]
                        },
                        isMD ? 'markdown' : 'file-code'
                    );

                    if (isMD && details.jump === true) {
                        item.isMarkdownFile = true;
                        item.relPath = relFilePath;
                    }
                    items.push(item);
                }
            }
            return items;
        }
    };
    vscode.window.registerTreeDataProvider('flexion-help', helpProvider);

    // 3. COMMANDS
    context.subscriptions.push(
        vscode.commands.registerCommand('flexion.openWiki', (rel) => {
            const uri = vscode.Uri.file(path.join(context.extensionPath, 'panel', rel));
            vscode.commands.executeCommand('markdown.showPreview', uri);
        }),
        vscode.commands.registerCommand('flexion.jumpToWikiSection', (rel, frag) => {
            const uri = vscode.Uri.file(path.join(context.extensionPath, 'panel', rel)).with({ fragment: frag });
            vscode.commands.executeCommand('markdown.showPreview', uri);
        }),
        vscode.commands.registerCommand('flexion.openExample', (rel) => {
            const uri = vscode.Uri.parse(`flexion-sample:/panel/${rel}`);
            vscode.window.showTextDocument(uri);
        })
    );

    // 4. HOVERS
    const typesMap = {
        'string': 'Sequence of characters.', 'str': 'Alias for string.',
        'int': 'Whole number.', 'integer': 'Alias for int.',
        'float': 'Decimal number.', 'decimal': 'Alias for float.', 'double': 'Alias for float.',
        'bool': 'Boolean (true/false).', 'boolean': 'Alias for bool.',
        'void': 'Empty/Null.', 'null': 'Alias for void.', 'undefined': 'Alias for void.',
        'object': 'Key-value collection.', 'list': 'Ordered collection.', 'array': 'Alias for list.',
        'keyword': 'Unquoted alphanumeric string.'
    };

    context.subscriptions.push(vscode.languages.registerHoverProvider('flexion', {
        provideHover(document, position) {
            const range = document.getWordRangeAtPosition(position, /"([^"\\]|\\.)*"|\$\(.*?\)|[@#\w/.-]+/);
            if (!range) return null;
            const word = document.getText(range);
            const lineText = document.lineAt(position.line).text;
            
            if (word.startsWith('$(')) {
                const typeBeforeExpr = lineText.match(new RegExp(`\\b(${Object.keys(typesMap).join('|')}):\\s*\\$\\(`));
                return new vscode.Hover(`**Evaluated Expression**\n\nInterpreted as: \`${typeBeforeExpr ? typeBeforeExpr[1] : 'auto'}\``);
            }

            const typeMatch = lineText.match(new RegExp(`\\b(${Object.keys(typesMap).join('|')}):\\s*${word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`));
            if (typeMatch) return new vscode.Hover(`Type: \`${typeMatch[1]}\``);
            if (typesMap[word]) return new vscode.Hover(`**Flexion Type**: ${typesMap[word]}`);
            
            return null;
        }
    }));

    // 5. NAVIGATION
    context.subscriptions.push(vscode.languages.registerDefinitionProvider('flexion', {
        provideDefinition(doc, pos) {
            const range = doc.getWordRangeAtPosition(pos, /(@templates\s+)?([@#\w/]+)/);
            if (!range) return null;
            const text = doc.getText(range);
            if (text.startsWith('@templates')) return findLocation(doc, text, 'toUsage');
            if (text.startsWith('@') || text.startsWith('#')) return findLocation(doc, text, 'toDefinition');
            return null;
        }
    }));

    // 6. AUTOCOMPLETE
    context.subscriptions.push(vscode.languages.registerCompletionItemProvider('flexion', {
        provideCompletionItems: () => Object.keys(typesMap).map(t => new vscode.CompletionItem(t, vscode.CompletionItemKind.Type))
    }, ':'));
}

module.exports = { activate, deactivate: () => {} };