import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { fileURLToPath } from 'node:url';
const transport = new StdioClientTransport({
  command: process.execPath,
  args: [fileURLToPath(new URL('node_modules/@satelliteoflove/godot-mcp/dist/cli.js', import.meta.url))],
  env: { ...process.env, GODOT_HOST: '127.0.0.1', GODOT_PORT: '6550', GODOT_MCP_USAGE_LOG: '0' },
  stderr: 'inherit',
});
const client = new Client({ name: 'reef-integration-smoke', version: '1.0.0' });
try {
  await client.connect(transport);
  const server = client.getServerVersion();
  if (server?.version !== '4.1.11') throw new Error(`Unexpected server: ${JSON.stringify(server)}`);
  const { tools } = await client.listTools();
  if (!tools.some(t => t.name === 'godot_editor_read')) throw new Error('Missing editor tool');
  let state;
  const deadline = Date.now() + 20000;
  do {
    state = await client.callTool({ name: 'godot_editor_read', arguments: { action: 'get_state' } });
    if (!state.isError || !JSON.stringify(state).includes('Not connected to Godot')) break;
    await new Promise(resolve => setTimeout(resolve, 500));
  } while (Date.now() < deadline);
  if (state.isError) throw new Error(JSON.stringify(state));
  const body = JSON.stringify(state);
  if (!body.includes('4.7.2')) throw new Error(`Wrong or missing editor version: ${body}`);
  console.log(JSON.stringify({ result: 'PASS', server, tool_count: tools.length, state }, null, 2));
} finally {
  await client.close();
}
