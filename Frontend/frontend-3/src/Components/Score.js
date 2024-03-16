import { Tooltip, ResponsiveContainer, Pie, PieChart, Cell, CartesianGrid, RadarChart, PolarRadiusAxis, Legend, Radar } from 'recharts';
import { health_fake } from '../Constants/fakeData';
import "./Score.css"

const COLORS = [
    "var(--primary-accent-color)",
    "var(--primary-accent-color)",
    "var(--primary-accent-color)",
    // "var(--primary-accent-color)",
    "yellow",
    "yellow",
    "rgb(255, 100, 100)"
    // "var(--secondary-accent-color)"
];

const Score = () => {
    // Score == logarithmic weighting of each score distance from baseline

    const calculateScore = (data) => {
        let score = 0;
        data.forEach(element => {
            score += element.value;
        });
        return score;
    }


    return (
        <div className="chart-title-container" id="Score">
            <div className="chart-title">Health Score</div>
            <div className="chart-row-container">
                <div className="chart-dingo-container">
                    <h6>Overall Score: {calculateScore(health_fake)}</h6>
                    <ol className="score-readout">
                        {health_fake.map((item, index) => {
                            return (
                                <li key={index}>
                                    <div className="score-value"
                                        style={{ color: COLORS[index % COLORS.length] }}
                                    >{item.name}:{item.value}</div>
                                </li>
                            )
                        })}
                    </ol>
                </div>
                < ResponsiveContainer className='chart-container' minHeight="40vh">
                    <PieChart className="chart">
                        <Pie
                            dataKey="value"
                            startAngle={180}
                            endAngle={0}
                            data={health_fake}
                            outerRadius={80}
                            innerRadius={70}
                            cx="50%"
                            cy="50%"
                            label
                        >
                            {health_fake.map((entry, index) => (
                                <Cell key={`cell-${index}`}
                                    fill={COLORS[index % COLORS.length]}
                                    stroke={COLORS[index % COLORS.length]}
                                    fillOpacity={0.7}
                                    strokeOpacity={1}
                                />
                            ))}
                        </Pie>
                        <Tooltip contentStyle={{
                            backgroundColor: "rgb(34, 34, 34)",
                        }}
                            itemStyle={{ color: "var(--primary-font-color" }}
                        />
                    </PieChart>
                </ResponsiveContainer >
                {/* TODO: add radar option and slider */}
            </div>
        </div>
    )
}

export default Score