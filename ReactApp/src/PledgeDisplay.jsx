/******************************************************************************
 *    Author: Michael Frohlich
 *      Date: 2019
 * Copyright: 2019 Michael Frohlich - Modified BSD License
 *****************************************************************************/

import React, { useEffect, useState } from 'react';

import Config from './Config';

export default function(props) {
    var nf = new Intl.NumberFormat();

    const [curVal, setVal] = useState(0);
    const [interval, setIntervalId] = useState(null);

    useEffect(() => {
        const f = async function() {
            console.log(props.badgeType, props.currencyType);
            let res = await fetch(
                Config.apiEndpoint +
                    `/getTotal/${props.badgeType}/${props.currencyType}/`,
            );

            // total currency is summed and returned from server
            res = await res.text();

            let val = parseInt(res);
            if (val > Config.goal) {
                val = Config.goal;
            }
            setVal(val);
        };

        if (interval != null) {
            clearInterval(interval);
        }
        setIntervalId(setInterval(f, Config.apiInterval));
    }, [props.badgeType, props.currencyType]);

    return (
        <div className="pledge-container bright-text">
            <div className="pledge-title">
                <div className={'icon'}>
                    <img src={props.icon} />
                </div>
                <div style={{ paddingLeft: '50px' }}>{nf.format(curVal)}</div>
            </div>
            <div className="pledge-subtitle gray-text">
                pledged of{' '}
                <span className="bright-text">{nf.format(props.goal)}</span>{' '}
                goal
            </div>
        </div>
    );
}
