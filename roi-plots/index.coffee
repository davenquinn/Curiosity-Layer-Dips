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
import StereonetComponent from './stereonet'

getData = (fn)->
  console.log fn
  filename = require.resolve(fn)
  attitudes = JSON.parse(readFileSync(filename))
  return nest()
    .key (d)->d.sol
    .entries attitudes

thresholdFilter = (threshold)-> (d)->
  # Remove data with a shorter axis length to err ratio
  x_ratio = d.axis_length[0]/d.axis_error[0]
  y_ratio = d.axis_length[1]/d.axis_error[1]
  console.log x_ratio, y_ratio
  return x_ratio > threshold and y_ratio > threshold

Plot = (props)->
  {type} = props
  type ?= 'no-errors'
  data = getData("../output/roi-models/attitudes-#{type}.json")

  h 'div.plots', data.map (d)->
    {key, values} = d

    filter = thresholdFilter(3)
    mainData = values.filter (d)->
      return false if d.stacked
      return filter(d)

    stackedData = values.filter (d)->
      return d.stacked

    h 'div.sol-plot', [
      h 'h2.sol', "Sol #{key}"
      h StereonetComponent, {data: mainData, stackedData}
    ]

Plot.propTypes = {}

module.exports = Plot
