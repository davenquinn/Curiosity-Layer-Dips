import h from 'react-hyperscript'
# Need some sort of CSS or else we get an error in bundler
import attitudes from './attitude-data.json'
import Promise from 'bluebird'
import chroma from 'chroma-js'
import * as d3 from 'd3'
require 'd3-selection-multi'
import 'd3-jetpack'
import {Stereonet} from '../webapp/Attitude/js-frontend/lib/attitude.js'
import {nest} from 'd3-collection'
import {Component} from 'react'
import {findDOMNode} from 'react-dom'
import './main.styl'

class StereonetComponent extends Component
  render: ->
    h 'svg.stereonet', {width: 340, height: 340}

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
      .attr 'stroke-width', '1px'
      .attr 'stroke', '#aaa'
      .attr 'stroke-dasharray', '2,2'

    stereonet.ellipses data

    stereonet.draw()

    svg.selectAll '.poles .normal .error'
      .attr 'fill', (d)->
        {area} = d.properties
        opacity = (2-area)*(2-area)/60
        "rgba(80,80,80,#{opacity})"
      .attr 'stroke', 'rgba(80,80,80,0.4)'


fn = =>

  groupedData = nest()
    .key (d)->d.sol
    .entries attitudes

  h 'div.plots', groupedData.map (d)->
    {key, values} = d
    h 'div.sol-plot', [
      h 'h2.sol', "Sol #{key}"
      h StereonetComponent, {data: values}
    ]

module.exports = fn
