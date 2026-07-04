#!/usr/bin/env node

const { runNastech } = require("../lib/python-launcher");

runNastech("nastech", process.argv.slice(2));
