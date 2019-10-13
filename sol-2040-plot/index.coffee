import util from 'util'
import {resolve} from 'path'
import {Component} from 'react'
import h from '@macrostrat/hyper'

exec = util.promisify(require('child_process').exec)

script = resolve './parse-roi-data.py'

class PlotComponent extends Component
  constructor: (props)->
    super props
    @state = {data: null}
    @getData()
  render: ->
    h 'div'

  getData: ->
    console.log "Getting data"
    {stdout, stderr} = await exec("pipenv run python #{script}")
    data = JSON.parse(stdout)
    @setState {data}
    console.log data

export default PlotComponent
