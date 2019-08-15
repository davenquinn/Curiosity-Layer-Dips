import h from 'react-hyperscript'
# Need some sort of CSS or else we get an error in bundler
import './main.styl'

fn = =>
  h 'div', 'Hello, world'

module.exports = fn
