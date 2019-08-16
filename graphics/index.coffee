import h from 'react-hyperscript'
# Need some sort of CSS or else we get an error in bundler
import data from './attitude-data.json'
import Promise from 'bluebird'
import chroma from 'chroma-js'
import * as d3 from 'd3'
require 'd3-selection-multi'
import 'd3-jetpack'
import {Stereonet} from '../webapp/Attitude/js-frontend/lib/attitude.js'
import {nest} from 'd3-collection'
import {Component} from 'react'
import {findDOMNode} from 'react-dom'

class StereonetComponent extends Component
  render: ->
    h 'svg.stereonet', {width: 400, height: 400}

  componentDidMount: ->
    {data} = @props
    el = findDOMNode(@)
    innerSize = {
      height: 300
      width: 300
    }

    stereonet = Stereonet()
      .size 300
      .margin 20
      .graticule 30, 5
      .clipAngle 20
      .rectangular(innerSize)

    svg = d3.select(el)
      .append 'g'
    svg.call stereonet

    stereonet
      .projection()
      .translate([170,170])

    svg.select '.neatline'
      .attr 'fill', 'transparent'
      .attr 'stroke-width', '2px'

    svg.select '.graticule'
      .attr 'fill', 'transparent'
      .attr 'stroke-width', '2px'
      .attr 'stroke', '#aaa'


    stereonet.ellipses data
    #.each setStyle
    stereonet.draw()


fn = =>

  groupedData = nest()
    .key (d)->d.sol
    .entries data

  h 'div', groupedData.map (data)->
    {key, values} = data
    h 'div', [
      h 'h2.sol', "Sol #{key}"
      h StereonetComponent, {data: values}

    ]

module.exports = fn
