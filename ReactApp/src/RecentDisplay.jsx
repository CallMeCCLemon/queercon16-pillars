/******************************************************************************
 *    Author: Michael Frohlich
 *      Date: 2019
 * Copyright: 2019 Michael Frohlich - Modified BSD License
 *****************************************************************************/

import React, { useEffect, useState } from 'react';

import Config from './Config';

export default function(props) {
    const [curRecents, setRecents] = useState([]);
    const [interval, setIntervalId] = useState(null);

    useEffect(() => {
        const f = async function() {
            let res = await fetch(
                Config.apiEndpoint +
                    `/recent/${props.currencyType}/${props.currencyType + 3}/${
                        Config.recent_limit
                    }/`,
            );

            // total currency is summed and returned from server
            res = await res.text();

            setRecents(JSON.parse(res));
        };

        if (interval != null) {
            clearInterval(interval);
        }
        setIntervalId(setInterval(f, Config.apiInterval));
    }, [props.badgeType, props.currencyType]);

    const entries = curRecents.map((v, i) => {
        return (
            <tr key={i}>
                <td>{v.badge_id}</td>
                <td>{v.badge_type}</td>
                <td>
                    <div className="currency-display">
                        <div className={'icon-small'}>
                            <img src={Config.icons[v.currency_type]} />
                        </div>
                        <div style={{ paddingLeft: '5px' }}>{v.quantity}</div>
                    </div>
                </td>
            </tr>
        );
    });
    return (
        <table className="recent-container">
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Type</th>
                    <th>Amount</th>
                </tr>
            </thead>
            <tbody>{entries}</tbody>
        </table>
    );
}
