const parser = require('@babel/parser');
const traverse = require('@babel/traverse').default;
const { resolve, dirname } = require('path');
const t = require('@babel/types');
const fs = require('fs');

// Define the base path
const basePath = resolve(dirname(__filename), './test');

function resolveFilePath(directory, relativePath) {
  const jsPath = resolve(directory, `${relativePath}.js`);
  const jsxPath = resolve(directory, `${relativePath}.jsx`);
  return fs.existsSync(jsPath) ? jsPath : fs.existsSync(jsxPath) ? jsxPath : null;
}

// Initialize an object to hold the file representation
const fileRepresentation = {};

// Initialize a set to hold the paths of traversed files
const traversedFiles = new Set();

// Helper function to ensure file representation initialization
function ensureFileRepresentation(filePath) {
  if (!fileRepresentation[filePath]) {
    fileRepresentation[filePath] = { imports: [], functions: [], classes: [], variables: [] };
  }
}

function traverseFile(filePath) {
  // If the file has already been traversed, return early to avoid infinite recursion
  if (traversedFiles.has(filePath)) {
    return;
  }

  // Mark the file as traversed
  traversedFiles.add(filePath);

  ensureFileRepresentation(filePath);
  const code = fs.readFileSync(filePath, 'utf-8');
  const ast = parser.parse(code, {
    sourceType: 'module',
    plugins: ['jsx'],
  });

  traverse(ast, {
    enter(path) {
      const node = path.node;
      if (t.isImportDeclaration(node)) {
        const sourcePath = resolveFilePath(dirname(filePath), node.source.value);
        if (sourcePath) {
          fileRepresentation[filePath].imports.push(sourcePath);
          traverseFile(sourcePath);
        }
      } else if (t.isFunctionDeclaration(node)) {
        const functionName = node.id.name;
        fileRepresentation[filePath].functions.push(functionName);
      } else if (t.isClassDeclaration(node)) {
        const className = node.id.name;
        fileRepresentation[filePath].classes.push(className);
      } else if (t.isVariableDeclaration(node)) {
        node.declarations.forEach(declaration => {
          if (t.isIdentifier(declaration.id)) {
            const variableName = declaration.id.name;
            fileRepresentation[filePath].variables.push(variableName);
          }
        });
      }
    },
  });
}

// Call the traverseFile function to build the file representation
const initialFilePath = resolve(basePath, 'index.js');
traverseFile(initialFilePath);

// Output the file representation
const outputPath = resolve(__dirname, 'output.json');
fs.writeFileSync(outputPath, JSON.stringify(fileRepresentation, null, 2), 'utf-8');

console.log(`File representation written to ${outputPath}`);

const commonPrefix = "/home/nitr0gen/ibrain.codes.next/components/ast_js/src/test/";

function shortenPath(path) {
  return path.replace(commonPrefix, "");
}

function abbreviateKeys(obj) {
  return {
    i: obj.imports.map(shortenPath),  // 'i' for imports
    f: obj.functions,                  // 'f' for functions
    c: obj.classes,                    // 'c' for classes
    v: obj.variables                   // 'v' for variables
  };
}

const compressedRepresentation = {};
for (const [key, value] of Object.entries(fileRepresentation)) {
  const shortKey = shortenPath(key);
  compressedRepresentation[shortKey] = abbreviateKeys(value);
}

// Now compressedRepresentation contains your compressed data structure

// To write it to a JSON file:
fs.writeFileSync('compressedOutput.json', JSON.stringify(compressedRepresentation, null, 0));

// Assume this function generates embeddings from code string
function generateEmbeddings(codeStr) {
  // Replace with real embeddings generation logic
  return [0.1, 0.2, 0.3];
}




function extractFunctionInfo(path, codeStr) {
  const { start, end } = path.node;
  const functionCode = codeStr.slice(start, end);
  const metadata = {
    name: path.node.id ? path.node.id.name : null,
    params: path.node.params.map(param => param.name),
    loc: path.node.loc
  };
  const embeddings = generateEmbeddings(functionCode);

  return {
    metadata,
    content: functionCode,
    embeddings
  };
}
function processFile(filePath) {
  if (!filePath) {
    throw new Error('File path is undefined or null');
  }

  const codeStr = fs.readFileSync(commonPrefix + filePath, 'utf8');
  const ast = parser.parse(codeStr, {
    sourceType: "module",
    plugins: ["jsx"]  // Add other plugins if necessary
  });

  const functionsInfo = [];
  traverse(ast, {
    FunctionDeclaration(path) {
      functionsInfo.push(extractFunctionInfo(path, codeStr));
    }
  });

  return functionsInfo;
}

function traverseGraph(nodeKey, graph) {
  const node = graph[nodeKey];
  if (node?.visited) return;
  node.visited = true;

  const functionsInfo = processFile(nodeKey);  // Assuming nodeKey is the file path
  node.functionsInfo = functionsInfo;

  node.i.forEach(dependency => {
    traverseGraph(dependency, graph);
  });
}


// Your graph data
const graph = compressedRepresentation;  // Replace with your graph data
const startingNode = 'index.js';
traverseGraph(startingNode, graph);

// Optionally, save the updated graph to a file
fs.writeFileSync('updatedGraph.json', JSON.stringify(graph, null, 2));
