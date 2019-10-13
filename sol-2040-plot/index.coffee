import {exec} from 'child_process'
import Promise from 'bluebird'
import {resolve} from 'path'

script = resolve './parse-roi-data.py'
runCommand = Promise.promisify(exec)

module.exports = (el, opts, cb)->
  console.log script

