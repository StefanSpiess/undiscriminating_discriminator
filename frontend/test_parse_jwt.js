const assert = require('assert');
const parseJwt = require('./parse_jwt');

// Example token with payload {"sub":"1234567890","name":"John Doe","admin":true}
const token =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.' +
  'eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.' +
  'signature';

const decoded = parseJwt(token);
assert.strictEqual(decoded.name, 'John Doe');
assert.strictEqual(decoded.admin, true);

assert.strictEqual(parseJwt('bad'), null);

console.log('parseJwt tests passed');
