import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

interface BiasMetricCardProps {
  label: string;
  value: number;
  color?: string;
}

export default function BiasMetricCard({ 
  label, 
  value, 
  color = "rgba(106,16,16,0.6)" 
}: BiasMetricCardProps) {
  return (
    <div className="w-full p-2 space-x-6 bg-white bg-opacity-20 border-2 border-white border-opacity-20 rounded-lg flex items-center justify-center">
      <h1 className="text-white text-xl min-w-fit">{label}</h1>
      <CircularProgressbar
        className="max-w-20 max-h-20"
        value={value}
        text={`${Math.round(value)}%`}
        styles={buildStyles({
          pathColor: color,
          textColor: "#ffffff",
          trailColor: "rgba(255,255,255,0.2)",
          backgroundColor: "transparent",
        })}
        strokeWidth={15}
      />
    </div>
  );
}
