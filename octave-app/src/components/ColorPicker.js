import React from 'react'
import { HuePicker } from 'react-color'
import reactCSS from 'reactcss'

class ColorPicker extends React.Component {
    state = {
      word: 'Select a Mood',
      color: {
        r: '0',
        g: '255',
        b: '250',
        a: '1',
      },
    };
 
    onChange = (color) => {
        this.setState({ 
          color: color.rgb 
        })
        if(color.oldHue <= 42) {
          this.setState({word: 'anxious'})
        } else if (color.oldHue <= 96) {
          this.setState({word: 'joyful'})
        } else if (color.oldHue <= 160) {
          this.setState({word: 'energized'})
        } else if (color.oldHue <= 226) {
          this.setState({word: 'peaceful'})
        } else if (color.oldHue <= 274) {
          this.setState({word: 'sad'})
        } else if (color.oldHue <= 324) {
          this.setState({word: 'tired'})
        } else {
          this.setState({word: 'angry'})
        }
        
    };
 
    render() {
      const styles = reactCSS({
        'default': {
          color: {
           color: `rgba(${ this.state.color.r }, ${ this.state.color.g }, ${ this.state.color.b }, ${ this.state.color.a })`,
          },
        },
      });

      return (
        <div>
          <p style={ styles.color }>{this.state.word}</p>
          <HuePicker color={ this.state.color } onChange={ this.onChange } />
        </div>
      )
    }
}
 
export default ColorPicker