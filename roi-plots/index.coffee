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
  filename = require.resolve(fn)
  attitudes = JSON.parse(readFileSync(filename))
  console.log attitudes
  return nest()
    .key (d)->d.key
    .entries attitudes

module.exports = ->
  data = getData("../output/roi-plots/attitudes.json")

  h 'div.plots', data.map (d)->
    {key, values} = d
    h 'div.sol-plot', [
      h 'h2.sol', "Image #{key}"
      h StereonetComponent, {data: values, filterData: false}
    ]
