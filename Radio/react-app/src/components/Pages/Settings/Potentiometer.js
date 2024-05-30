import './Potentiometer.css'

export default function Potentiometer(props) {
    const mystyle = {
      float: "left",
      marginRight: "20px"
    };
      return (
        <div className="potentiometer">
          <input type="checkbox" name='on' id='on'/>
          <h3>{props.name}</h3>
          <section>
            <div style={mystyle}>
              <label for="minimum">Minimum</label>
              <input type="number" id="minimum" name="minimum" />
            </div>
          </section>
          <section>   
            <div style={{float:"left"}}>
              <label for="maximum">Maximum</label>
              <input type="number" id="maximum" name="maximum" />
            </div>
            <br style={{clear:"both"}} />
          </section>
          <section>
            <label for="pin" className='pinLabel'>Pin</label>
            <input type="number" id="pin" name="pin" value="False"/>
          </section>
          <section>
            <label for="formula" className='formulaLabel'> Formula</label>
            <input type="checkbox" id="formula" name="formula" value="False"/>
          </section>
          <div class="vertical-center">
              <button type="button" className="Delete">Delete</button>
          </div>
        </div>
    );
};