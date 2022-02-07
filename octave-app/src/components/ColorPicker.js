import React from 'react'
import { HuePicker } from 'react-color'

class ColorPicker extends React.Component {
    state = {
      showPicker: true,
      color: {
        r: '225',
        g: '155',
        b: '99',
        a: '2',
      },
    };
 
    onChange = (color) => {
        this.setState({ 
          color: color.rgb 
        })
    };
 
    render() {
      return (
        <HuePicker color={ this.state.color } onChange={ this.onChange } />
      )
    }
}
 
export default ColorPicker