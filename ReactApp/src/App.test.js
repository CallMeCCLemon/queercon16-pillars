/******************************************************************************
 *    Author: Michael Frohlich
 *      Date: 2019
 * Copyright: 2019 Michael Frohlich - Modified BSD License
 *****************************************************************************/

import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<App />, div);
  ReactDOM.unmountComponentAtNode(div);
});
