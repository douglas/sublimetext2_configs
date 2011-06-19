/**
 * Browser-like object for printing to stdout and stderr.
 */
var console = {};

/**
 * Same as console.log.
 */
console.info = function() {}

/**
 * Same as assert.ok().
 */
console.assert = function() {}

/**
 * Prints to stdout with newline. This function can take multiple arguments
 * in a printf()-like way. Example:
 */
console.log = function() {}

/**
 * Print a stack trace to stderr of the current position.
 */
console.trace = function() {}

/**
 * Same as console.log but prints to stderr.
 */
console.error = function() {}

/**
 * Finish timer, record output. Example
 */
console.timeEnd = function() {}

console.warn = function() {}

/**
 * Mark a time.
 */
console.time = function() {}

/**
 * Uses util.inspect on obj and prints resulting string to stderr.
 */
console.dir = function() {}


exports = console;

