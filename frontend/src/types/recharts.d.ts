// Recharts Type Declarations - JAC Learning Platform
// Author: Cavin Otieno

declare module 'recharts' {
  import { ComponentType, ReactNode } from 'react';

  export interface ChartProps {
    width?: number | string;
    height?: number | string;
    data?: any[];
    margin?: {
      top?: number;
      right?: number;
      bottom?: number;
      left?: number;
    };
    syncId?: string;
    className?: string;
    children?: ReactNode;
    layout?: 'horizontal' | 'vertical';
    stackOffset?: 'none' | 'expand' | 'wiggle' | 'silhouette';
    barCategoryGap?: number | string;
    barGap?: number | string;
    maxBarSize?: number;
  }

  export interface AxisProps {
    dataKey?: string;
    domain?: [number | string | ((dataMin: number) => number), number | string | ((dataMax: number) => number)];
    type?: 'number' | 'category';
    allowDataOverflow?: boolean;
    allowDuplicatedCategory?: boolean;
    allowDecimals?: boolean;
    allowTickFormatting?: boolean;
    axisLine?: boolean | React.CSSProperties;
    className?: string;
    tick?: boolean | ComponentType<any> | ReactNode | React.CSSProperties;
    tickFormatter?: (value: any, index: number) => string;
    tickLine?: boolean | React.CSSProperties;
    tickMargin?: number;
    tickSize?: number;
    interval?: number | 'preserveStart' | 'preserveEnd' | 'preserveStartEnd';
    angle?: number;
    fontSize?: number;
    fontFamily?: string;
    label?: string | number | ReactNode | ((props: any) => ReactNode);
    scale?: 'auto' | 'linear' | 'pow' | 'sqrt' | 'log' | 'identity' | 'time' | 'band' | 'point' | 'ordinal' | 'quantile' | 'quantize' | 'utc' | 'sequential' | 'threshold';
    tickCount?: number;
    unit?: string | number;
    name?: string | number;
    width?: number;
    height?: number;
    orientation?: 'left' | 'right' | 'middle' | 'top' | 'bottom';
    yAxisId?: string | number;
    xAxisId?: string | number;
    reversed?: boolean;
  }

  export interface TooltipProps {
    active?: boolean;
    coordinate?: { x?: number; y?: number };
    cursor?: boolean | ComponentType<any> | React.CSSProperties;
    separator?: string;
    offset?: number;
    filterNull?: boolean;
    itemStyle?: React.CSSProperties;
    contentStyle?: React.CSSProperties;
    labelStyle?: React.CSSProperties;
    cursorStyle?: React.CSSProperties;
    viewBox?: { x?: number; y?: number; width?: number; height?: number };
    labelFormatter?: (label: any, payload: any[]) => ReactNode;
    itemFormatter?: (value: any, name: any, props: any) => ReactNode;
    position?: { x?: number; y?: number };
    wrapperStyle?: React.CSSProperties;
    content?: ComponentType<any>;
  }

  export interface ResponsiveContainerProps {
    aspect?: number;
    width?: string | number;
    height?: string | number;
    minHeight?: number;
    maxHeight?: number;
    minWidth?: number;
    maxWidth?: number;
    children?: ReactNode;
    debounce?: number;
  }

  export interface LegendProps {
    content?: ComponentType<any>;
    wrapperStyle?: React.CSSProperties;
    chartWidth?: number;
    chartHeight?: number;
    iconSize?: number;
    iconType?: 'line' | 'plainline' | 'square' | 'rect' | 'circle' | 'cross' | 'diamond' | 'star' | 'triangle' | 'wye';
    layout?: 'horizontal' | 'vertical';
    margin?: {
      top?: number;
      left?: number;
      bottom?: number;
      right?: number;
    };
    payload?: any[];
    verticalAlign?: 'top' | 'middle' | 'bottom';
    align?: 'left' | 'center' | 'right';
  }

  export interface BarProps {
    dataKey: string;
    fill?: string;
    stroke?: string;
    strokeWidth?: number;
    maxBarSize?: number;
    minPointSize?: number;
    stackId?: string;
    radius?: number | [number, number, number, number];
    name?: string;
    legendType?: 'line' | 'rect' | 'circle' | 'cross' | 'diamond' | 'square' | 'star' | 'triangle' | 'wye';
  }

  export interface LineProps {
    type?: 'basis' | 'basisClosed' | 'basisOpen' | 'linear' | 'linearClosed' | 'natural' | 'monotoneX' | 'monotoneY' | 'monotone' | 'step' | 'stepBefore' | 'stepAfter';
    dataKey: string;
    stroke?: string;
    strokeWidth?: number;
    fill?: string;
    fillOpacity?: number;
    strokeDasharray?: string;
    strokeOpacity?: number;
    strokeLinecap?: 'butt' | 'round' | 'square';
    strokeLinejoin?: 'miter' | 'round' | 'bevel';
    dot?: boolean | ComponentType<any> | React.CSSProperties;
    activeDot?: boolean | ComponentType<any> | React.CSSProperties;
    legendType?: 'line' | 'rect' | 'circle' | 'cross' | 'diamond' | 'square' | 'star' | 'triangle' | 'wye';
    connectNulls?: boolean;
    name?: string;
  }

  // Chart Components
  export const LineChart: ComponentType<ChartProps>;
  export const BarChart: ComponentType<ChartProps>;
  export const AreaChart: ComponentType<ChartProps>;
  export const ComposedChart: ComponentType<ChartProps>;
  export const RadarChart: ComponentType<ChartProps>;
  export const ScatterChart: ComponentType<ChartProps>;
  export const PieChart: ComponentType<ChartProps>;

  // Axis Components
  export const XAxis: ComponentType<AxisProps>;
  export const YAxis: ComponentType<AxisProps>;

  // Utility Components
  export const CartesianGrid: ComponentType<{ stroke?: string; strokeDasharray?: string; strokeWidth?: number; }>;
  export const Tooltip: ComponentType<TooltipProps>;
  export const Legend: ComponentType<LegendProps>;
  export const ResponsiveContainer: ComponentType<ResponsiveContainerProps>;

  // Shape Components
  export const Line: ComponentType<LineProps>;
  export const Bar: ComponentType<BarProps>;
  export const Area: ComponentType<{
    type?: string;
    dataKey: string;
    stroke?: string;
    fill?: string;
    fillOpacity?: number;
    strokeWidth?: number;
    stackId?: string;
    name?: string;
  }>;
  export const Radar: ComponentType<{
    dataKey: string;
    stroke?: string;
    fill?: string;
    fillOpacity?: number;
    strokeWidth?: number;
    name?: string;
  }>;
  export const Scatter: ComponentType<{
    dataKey: string;
    fill?: string;
    name?: string;
  }>;
  export const Pie: ComponentType<{
    dataKey: string;
    cx?: string | number;
    cy?: string | number;
    innerRadius?: number;
    outerRadius?: number;
    fill?: string;
    data?: any[];
    name?: string;
    legendType?: string;
  }>;
  export const Cell: ComponentType<{ fill?: string; stroke?: string; strokeWidth?: number; }>;

  // Polar Components
  export const PolarGrid: ComponentType<{ cx?: number; cy?: number; innerRadius?: number; outerRadius?: number; polarAngles?: number[]; polarRadius?: number[]; gridType?: string; radialLines?: boolean; }>;
  export const PolarAngleAxis: ComponentType<{ cx?: number; cy?: number; radius?: number; axisLineType?: string; dataKey?: string; tick?: boolean | ComponentType<any> | React.CSSProperties; tickFormatter?: (value: any, index: number) => string; className?: string; }>;
  export const PolarRadiusAxis: ComponentType<{ cx?: number; cy?: number; orientation?: 'left' | 'right' | 'middle'; axisLineType?: string; tick?: boolean | ComponentType<any> | React.CSSProperties; tickFormatter?: (value: any, index: number) => string; domain?: [number | string, number | string]; tickCount?: number; className?: string; }>;
}