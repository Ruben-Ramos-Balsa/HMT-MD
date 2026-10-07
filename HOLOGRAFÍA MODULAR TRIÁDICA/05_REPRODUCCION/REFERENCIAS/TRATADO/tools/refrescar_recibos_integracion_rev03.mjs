import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import {fileURLToPath} from "node:url";

const base = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const args = process.argv.slice(2);
if(args.includes("--help")){
  console.log("Usage: node refrescar_recibos_integracion_rev03.mjs [--build BUILD_DIR]\nBUILD_DIR defaults to HMT_BUILD_DIR or REV03/build. Relative paths resolve within REV03. This refreshes documentary bindings, not mathematical admission.");
  process.exit(0);
}
const buildArg = args.indexOf("--build");
if(args.length!==0&&(args.length!==2||args[0]!=="--build"||!args[1])){
  console.error("Expected only --build BUILD_DIR");process.exit(2);
}
const configuredBuild = buildArg>=0?args[buildArg+1]:(process.env.HMT_BUILD_DIR||"build");
const buildDir = path.isAbsolute(configuredBuild)?configuredBuild:path.resolve(base,configuredBuild);
const metadata = path.join(base,"metadata");
const v4path = path.join(metadata,"RECIBO_GENEALOGICO_INTEGRACION_REV03_V4.json");
const causalPath = path.join(metadata,"RECIBO_CAUSAL_INTEGRACION_REV03_1_1.json");
const invPath = path.join(metadata,"INVENTARIO_GENEALOGICO_INTEGRACION_REV03.json");
const source = path.join(base,"source");
const sha = p => crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
const countLines = p => {
  const t=fs.readFileSync(p,"utf8");
  return t ? t.replace(/\n$/,"").split("\n").length : 0;
};
const read = p => JSON.parse(fs.readFileSync(p,"utf8"));
const save = (p,o) => fs.writeFileSync(p,JSON.stringify(o,null,2)+"\n");
const v4=read(v4path), causal=read(causalPath), inventory=read(invPath);
const changes=[],errors=[];
function refresh(obj,location=""){
  if(!obj||typeof obj!=="object")return;
  if(Array.isArray(obj)){obj.forEach((x,i)=>refresh(x,location+"["+i+"]"));return;}
  if(typeof obj.path==="string"&&typeof obj.sha256==="string"){
    if(!path.isAbsolute(obj.path)||!fs.existsSync(obj.path)){
      errors.push({location,path:obj.path,error:"SOURCE_MISSING"});return;
    }
    const digest=sha(obj.path);
    if(obj.sha256!==digest)changes.push({location,path:obj.path,previous:obj.sha256,current:digest});
    obj.sha256=digest;
    if(typeof obj.lines==="string"){
      const match=obj.lines.match(/^(\d+)(?:-(\d+))?$/);
      if(match){const end=Number(match[2]||match[1]),n=countLines(obj.path);
        if(end>n)errors.push({location,path:obj.path,error:"LINE_RANGE_OUTSIDE_SOURCE",range:obj.lines,actual_lines:n});
      }
    }
    if("line_count" in obj)obj.line_count=countLines(obj.path);
  }
  for(const [k,value]of Object.entries(obj))if(k!=="source_snapshot")refresh(value,location+"."+k);
}
refresh(v4,"v4");refresh(causal,"causal");refresh(inventory,"inventory");
const manifest=[];
function walk(dir){for(const entry of fs.readdirSync(dir,{withFileTypes:true})){
  const p=path.join(dir,entry.name);
  if(entry.isDirectory())walk(p);
  else if(entry.isFile()&&/\.(tex|bib|sty|cls|bbl)$/.test(entry.name))
    manifest.push({path:p,sha256:sha(p),lines:countLines(p)});
}}
walk(source);manifest.sort((a,b)=>a.path.localeCompare(b.path));
const flsPath=path.join(buildDir,"main.fls");
const flsText=fs.existsSync(flsPath)?fs.readFileSync(flsPath,"utf8"):"";
if(!flsText)errors.push({path:flsPath,error:"FLS_MISSING_OR_EMPTY"});
const pwd=flsText.split("\n").find(x=>x.startsWith("PWD "))?.slice(4);
const inputPaths=new Set(flsText.split("\n").filter(x=>x.startsWith("INPUT ")).map(x=>{
 const p=x.slice(6);return path.resolve(pwd||base,p);
}));
const localInputs=manifest.filter(x=>inputPaths.has(x.path));
const evidenceInFls=inventory.evidence.map(e=>({id:e.id,path:e.path,in_current_fls:inputPaths.has(e.path)}));
const snapPath=path.join(metadata,"MANIFIESTO_FUENTES_INTEGRACION_REV03.json");
const stamp=new Date().toISOString();
const buildPdf=path.join(buildDir,"main.pdf");
const deliveredPdf=path.join(base,"output/pdf/HOLOGRAFIA_MODULAR_TRIADICA_20260919.pdf");
const pdfBinding={
 build_pdf:fs.existsSync(buildPdf)?{path:buildPdf,sha256:sha(buildPdf)}:null,
 output_copy:fs.existsSync(deliveredPdf)?{path:deliveredPdf,sha256:sha(deliveredPdf)}:null,
 byte_identity:fs.existsSync(buildPdf)&&fs.existsSync(deliveredPdf)?sha(buildPdf)===sha(deliveredPdf):null,
 scope:"Identidad documental observada; no certificación matemática ni sustituto del control visual.",
 final_admission:false
};
save(snapPath,{schema:"hmt-rev03-editorial-source-snapshot-v1",generated_at_utc:stamp,
 scope:"Instantánea local de fuentes; no validación matemática ni admisión final del PDF.",
 source_tree:source,build_directory:buildDir,files:manifest,source_file_count:manifest.length,local_fls_input_count:localInputs.length,
 fls:fs.existsSync(flsPath)?{path:flsPath,sha256:sha(flsPath),pwd}:null,
 pdf_binding:pdfBinding,
 evidence_in_fls:evidenceInFls,
 compilation_finality:"OBSERVED_SNAPSHOT_REQUIRES_FINAL_STABLE_COMPILATION"});
const binding={path:snapPath,sha256:sha(snapPath),generated_at_utc:stamp,
 source_file_count:manifest.length,local_fls_input_count:localInputs.length,
 final_admission:false,scope:"Esta huella vincula la edición observada, no la verdad de cada enunciado."};
v4.source_snapshot=binding;causal.source_snapshot=binding;
v4.documentary_pdf_binding=pdfBinding;causal.documentary_pdf_binding=pdfBinding;
v4.artifact.sha256=sha(v4.artifact.path);
causal.artifact_sha256=sha(causal.artifact);
const fresh = {generated_at_utc:stamp,build_directory:buildDir,fls_path:flsPath,status:errors.length?"FAIL_REFRESH_LOCATORS":"PASS_REFRESH_LOCATORS",
 changed_files:[...new Set(changes.map(x=>x.path))],changed_locator_bindings:changes,
 errors,semantic_rule:"Una variación de contenido requiere revisar el ámbito de su evidencia; la actualización de huella no constituye esa revisión.",
 evidence_missing_from_fls:evidenceInFls.filter(x=>!x.in_current_fls)};
save(v4path,v4);save(causalPath,causal);save(invPath,inventory);
save(path.join(metadata,"REFRESCO_RECIBOS_INTEGRACION_REV03.json"),fresh);
console.log(JSON.stringify({status:fresh.status,build_directory:buildDir,source_file_count:manifest.length,
 local_fls_input_count:localInputs.length,changed_files:fresh.changed_files.length,
 errors,evidence_missing_from_fls:fresh.evidence_missing_from_fls},null,2));
if(errors.length)process.exitCode=1;
