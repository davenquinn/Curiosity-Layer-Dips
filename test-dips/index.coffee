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
import {readFileSync} from 'fs'
import '../roi-plots/main.styl'
import StereonetComponent from '../roi-plots/stereonet'

getData = (fn)->
  console.log fn
  filename = require.resolve(fn)
  return JSON.parse(readFileSync(filename))

Plot = ->
  data = getData("./mappings.json")
  h StereonetComponent, {
    data,
    clipAngle: 60,
    graticule: [30,15]
    margin: 5
  }

Plot.propTypes = {}

module.exports = Plot

