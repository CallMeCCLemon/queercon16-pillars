/******************************************************************************
 *    Author: Michael Frohlich
 *      Date: 2019
 * Copyright: 2019 Michael Frohlich - Modified BSD License
 *****************************************************************************/

import React, { useEffect, useState } from 'react';
import './App.css';
import Config from './Config';

import PledgeDisplay from './PledgeDisplay.jsx';
import hotkeys from 'hotkeys-js';
import RecentDisplay from './RecentDisplay';

function App() {
    const [curCurrency, setCurrency] = useState(0);

    useEffect(() => {
        hotkeys('ctrl+a', function(event, handler) {
            // Prevent the default refresh event under WINDOWS system
            event.preventDefault();
            setCurrency((c) => {
                if (c + 1 == 3) {
                    return 0;
                } else {
                    return c + 1;
                }
            });
        });

        setCurrency(Config.currencyType);
    }, []);
    return (
        <div className="App">
            <div className="Padding" />
            <div className="Pledges">
                <PledgeDisplay
                    badgeType="Q"
                    currencyType={curCurrency}
                    goal={Config.goal}
                    icon={Config.icons[curCurrency]}
                />
                <PledgeDisplay
                    badgeType="C"
                    currencyType={curCurrency + 3}
                    goal={Config.goal}
                    icon={Config.icons[curCurrency + 3]}
                />
            </div>
            <div className="Recents">
                <div className="recents-title">Recent</div>
                <div className="divider-line" />
                <RecentDisplay currencyType={curCurrency} />
            </div>
            <div className="Padding" />
        </div>
    );
}

export default App;
