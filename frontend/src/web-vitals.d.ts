declare module 'web-vitals' {
    export type Metric = {
      id: string;
      name: string;
      value: number;
    };
  
    export type ReportHandler = (metric: Metric) => void;
  
    export function getCLS(onReport: ReportHandler, reportAllChanges?: boolean): void;
    export function getFID(onReport: ReportHandler): void;
    export function getFCP(onReport: ReportHandler): void;
    export function getLCP(onReport: ReportHandler, reportAllChanges?: boolean): void;
    export function getTTFB(onReport: ReportHandler): void;
  }