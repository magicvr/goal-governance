// Test-only SDK adapter. Its empty response is NOT a submitted human answer.
// No production provider configuration is modified or copied into evidence.
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const [fixtureArg, outputArg] = process.argv.slice(2);
const fixture = path.resolve(fixtureArg);
const output = path.resolve(outputArg);
if (!path.basename(fixture).startsWith('gg-goal013-s3-')) throw Error('Expected owned synthetic fixture');
const platform = 'C:/Users/magicvr/AppData/Roaming/npm/node_modules/@github/copilot/node_modules/@github/copilot-win32-x64';
const { CopilotClient, RuntimeConnection, approveAll } = await import(pathToFileURL(platform + '/copilot-sdk/index.js'));
const logFile = path.join(output, 'sdk-events.jsonl');
if (fs.existsSync(logFile)) throw Error('Refusing to replace prior SDK evidence');
fs.mkdirSync(output, { recursive: true });
const privateKeys = new Set(['reasoningText','reasoningContent','reasoning_content','thinking','thought','signature']);
function scrub(value) {
  if (Array.isArray(value)) return value.map(scrub);
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).filter(([k])=>!privateKeys.has(k)).map(([k,v])=>[k,scrub(v)]));
  return value;
}
function emit(event) { fs.appendFileSync(logFile, JSON.stringify({observedAt:new Date().toISOString(),...scrub(event)})+'\n'); }
const within = value => {
  const rel = path.relative(fixture, path.resolve(fixture, value));
  return rel === '' || (!path.isAbsolute(rel) && rel !== '..' && !rel.startsWith('..'+path.sep));
};
const client = new CopilotClient({connection:RuntimeConnection.forStdio({path:platform+'/copilot.exe'}),workingDirectory:fixture,logLevel:'none'});
let session;
let callbackCount=0;
try {
  await client.start();
  const status=await client.getStatus();
  emit({type:'probe-runtime',version:status.version,protocolVersion:status.protocolVersion,syntheticFixture:true,humanAnswerSubmitted:false,fixture});
  session=await client.createSession({
    model:'gemini-3.8-flash-high',workingDirectory:fixture,
    availableTools:['view','glob','grep','create','edit','skill','ask_user'],
    onPermissionRequest:(request, invocation)=>{
      const target=request.kind==='write'?request.fileName:request.kind==='read'?request.path:undefined;
      if(!target || !within(target)) {
        emit({type:'probe-permission-refused',kind:request.kind});
        throw Error('Synthetic probe only permits file read/write inside its fixture');
      }
      emit({type:'probe-permission-approved',kind:request.kind,path:target,notAUserAnswer:true});
      return approveAll(request,invocation);
    },
    onUserInputRequest:(request)=>{
      callbackCount++;
      const response={answer:'',wasFreeform:false};
      emit({type:'probe-user-input-callback',request,response,syntheticCallback:true,humanAnswerSubmitted:false});
      return response;
    },
  });
  session.on(event=>{
    if(['tool.execution_start','tool.execution_complete','assistant.message','session.idle','session.error'].includes(event.type)) emit(event);
  });
  const message=await session.sendAndWait('/govern 工作区2 GOAL-013，推进下一步。',600000);
  emit({type:'probe-completed',sessionId:session.sessionId,callbackCount,result:message?.data?.content??null,humanAnswerSubmitted:false});
} catch(error) {
  emit({type:'probe-error',errorType:error?.name,code:error?.code??null,callbackCount});
  await session?.abort().catch(()=>{});
  process.exitCode=1;
} finally {
  await client.stop();
}
