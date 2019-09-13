import h from 'react-hyperscript'
# Need some sort of CSS or else we get an error in bundler
import Promise from 'bluebird'
import chroma from 'chroma-js'
import * as d3 from 'd3'
require 'd3-selection-multi'
import 'd3-jetpack'
import {Stereonet} from '../deps/Attitude/js-frontend/lib/attitude.js'
import {nest} from 'd3-collection'
import {Component} from 'react'
import {findDOMNode, render} from 'react-dom'
import {readFileSync} from 'fs'
import './main.styl'
import {AzimuthLabels, DipLabels} from './graticule-labels'
import StereonetComponent from './stereonet'

getData = (fn)->
  filename = require.resolve(fn)
  attitudes = JSON.parse(readFileSync(filename))
  return nest()
    .key (d)->d.sol
    .entries attitudes

module.exports = (props)->
  {type, stacked} = props
  type ?= '1s'
  stacked ?= false

  filterData = true
  if stacked
    filterData = false

  mainData = getData("./mappings/attitudes-#{type}.json")
  stackedData = null
  if stacked
    stackedData = getData("./mappings/attitudes-#{type}-stacked.json")

  h 'div.plots', mainData.map (d)->
    {key, values} = d

    if stackedData?
      sv = stackedData.find (d)->d.key == key
      if sv?
        sv = sv.values

    #stackedData =
    h 'div.sol-plot', [
      h 'h2.sol', "Sol #{key}"
      h StereonetComponent, {data: values, stackedData: sv, filterData}
    ]
