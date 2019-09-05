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
import StereonetComponent from '../sol-plots/stereonet'

getData = (fn)->
  console.log fn
  filename = require.resolve(fn)
  attitudes = JSON.parse(readFileSync(filename))
  return nest()
    .key (d)->d.sol
    .entries attitudes

module.exports = (props)->
  {type} = props
  type ?= 'no-errors'
  data = getData("../output/roi-plots/attitudes-#{type}.json")

  h 'div.plots', data.map (d)->
    {key, values} = d
    h 'div.sol-plot', [
      h 'h2.sol', "Sol #{key}"
      h StereonetComponent, {data: values, filterData: false}
    ]