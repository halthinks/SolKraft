#!/usr/bin/env node
import { inspectRepository } from "../../../server/platform-delivery.mjs";

const root=process.argv[2];if(!root){console.error("Usage: inspect-repository.mjs <repository-root>");process.exit(64)}
console.log(JSON.stringify(await inspectRepository(root),null,2));
