import util from 'util'
import {resolve} from 'path'
import {Component} from 'react'
import h from '@macrostrat/hyper'
import StereonetComponent from './stereonet'
import roiData from './attitude-data.json'

class PlotComponent extends Component
  constructor: (props)->
    super props
    @state = {data: roiData}
  render: ->
    {data} = @state
    return null unless data?
    mainData = data.filter (d)->not d.stacked
    stackedData = data.filter (d)->d.stacked
    h StereonetComponent, {
      data: mainData,
      stackedData, filterData: false
      width: 600
      height: 300
    }

export default PlotComponent
