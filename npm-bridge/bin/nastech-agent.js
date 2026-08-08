#!/usr/bin/env node

const { runNastech } = require("../lib/python-launcher");

runNastech("nastech-agent", process.argv.slice(2));
