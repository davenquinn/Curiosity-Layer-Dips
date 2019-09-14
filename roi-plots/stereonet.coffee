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

class StereonetComponent extends Component
  @defaultProps: {
    filterData: false
    clipAngle: 20
    margin: 20
    size: 300
    graticule: [30, 5]
  }
  render: ->
    {size, margin} = @props
    v = size+2*margin
    h 'svg.stereonet', {width: v, height: v}

  componentDidMount: ->
    {data, stackedData, filterData,
     clipAngle, graticule, margin, size} = @props

    if filterData
      data = data.filter (d)->
        v = d.ratio_1 > 3 and d.ratio_2 > 3
        v

    el = findDOMNode(@)
    innerSize = {
      height: size
      width: size
    }

    stereonet = Stereonet()
      .size size
      .margin @props.margin
      .graticule(graticule...)
      .clipAngle clipAngle
      .rectangular(innerSize)

    svg = d3.select(el)
      .append 'g'
    svg.call stereonet

    stereonet
      .projection()
      .translate([innerSize.width/2+margin,innerSize.height/2+margin])

    svg.select '.neatline'
      .attr 'fill', 'transparent'
      .attr 'stroke-width', '2px'

    svg.select '.graticule'
      .attr 'fill', 'transparent'
      .attr 'stroke-width', '1px'
      .attr 'stroke', '#aaa'
      .attr 'stroke-dasharray', '2,2'

    ell2 = null
    if stackedData?
      ell2 = stereonet.ellipses stackedData
    ell = stereonet.ellipses data

    stereonet.draw()

    ell.each (d)->
      el = d3.select(@).select('.error')
      fill = 'transparent'
      #if d.min_angular_error < 10
      opacity = 1/d.min_angular_error/d.min_angular_error
      if opacity > 0.2
        opacity = 0.2
      if opacity < 0.05
        opacity = 0.05
      console.log opacity
      fill = "rgba(80,80,80,#{opacity})"
      #else
      #  el.attr 'stroke-dasharray', '4,2'
      el.attr 'fill', fill

    return unless ell2?

    ell2.each (d)->
      el = d3.select(@).select('.error')
      fill = 'transparent'
      #if d.min_angular_error < 10
      opacity = 1/d.min_angular_error/d.min_angular_error
      if opacity > 0.2
        opacity = 0.2
      if opacity < 0.05
        opacity = 0.05
      fill = "rgba(0,197,255,0.5)"
      #else
      #  el.attr 'stroke-dasharray', '4,2'
      el.attr 'fill', fill

export default StereonetComponent
