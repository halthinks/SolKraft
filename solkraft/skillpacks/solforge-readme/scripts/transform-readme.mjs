#!/usr/bin/env node
import { createHash } from "node:crypto";
import { access, mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { PUBLIC_SKILL_IDS } from "../../../server/capability-registry.mjs";
import { verifyFinalActionGoal } from "../../../server/autonomy-contract.mjs";
import { compileReadmePackage, createReadmeResultReceipt } from "../../../server/readme-transform.mjs";

const args=process.argv.slice(2);const [source,output,projectName,goalPromptFile,routeHash,routeReceiptSha256]=args;
if(!source||!output||!projectName||!goalPromptFile||!hash(routeHash)||!hash(routeReceiptSha256)){
  console.error("Usage: transform-readme.mjs <source.md> <new-output-directory> <project-name> <goal-prompt-file> <route-hash> <route-receipt-sha256>");process.exit(64);
}
const sourcePath=resolve(source),outputRoot=resolve(output);const sourceMarkdown=await readFile(sourcePath,"utf8");const goalPrompt=await readFile(resolve(goalPromptFile),"utf8");
const goalHash=createHash("sha256").update(goalPrompt).digest("hex");verifyFinalActionGoal({goalPrompt,goalPromptSha256:goalHash});
const action=goalPrompt.match(/^Action:\s*(.+)$/imu)?.[1]??"";if(!/^(?:write|create|generate|transform|produce)\b.*\bREADME\b/iu.test(action)||/\b(?:do not|don't|never)\b/iu.test(action))throw new Error("Goal Action must positively and explicitly direct the README package write");
const relativeSource=source.replaceAll("\\","/").replace(/^\.\//u,"");
const pkg=compileReadmePackage({sourceMarkdown,sourcePath:relativeSource,projectName,capabilityNames:PUBLIC_SKILL_IDS,requestId:`readme-${goalHash.slice(0,16)}`,goalHash,routeHash,routeReceiptSha256});
if(!pkg.validation.accepted){console.error(JSON.stringify({accepted:false,packageHash:pkg.packageHash,sourceHash:pkg.sourceHash,blockers:pkg.validation.blockers},null,2));process.exit(2)}
const targets=[...Object.keys(pkg.files),"readme-package.json","readme-result-receipt.json"].map(path=>resolve(outputRoot,path));
for(const target of targets)try{await access(target);throw new Error(`refusing to overwrite existing repository artifact: ${target}`)}catch(error){if(error?.code!=="ENOENT")throw error}
const receipt=createReadmeResultReceipt(pkg,{acceptedBy:`native-goal:${goalHash}`,acceptedAt:new Date().toISOString(),goalHash});
for(const [relativePath,text] of Object.entries(pkg.files)){const target=resolve(outputRoot,relativePath);await mkdir(dirname(target),{recursive:true});await writeFile(target,text,"utf8")}
await writeFile(resolve(outputRoot,"readme-package.json"),JSON.stringify(pkg,null,2)+"\n","utf8");
await writeFile(resolve(outputRoot,"readme-result-receipt.json"),JSON.stringify(receipt,null,2)+"\n","utf8");
console.log(JSON.stringify({packageHash:pkg.packageHash,receiptSha256:receipt.receiptSha256,goalHash,sourceHash:pkg.sourceHash,accepted:true,files:Object.keys(pkg.files)},null,2));

function hash(value){return /^[a-f0-9]{64}$/u.test(value??"")}
