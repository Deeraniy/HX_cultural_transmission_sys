import request from "@/utils/request";

const REPORT_BASE_URL = "";

class ReportAPI {
    // 生成宣传报告
    static generatePublicityReportAPI(data: {
        platform: string;
        title: string;
        content: string;
        tags: string[];
        eventName: string;
        eventType: string;
        promotionTendency: string;
        promotionMethod: string;
    }) {
        return request({
            url: `${REPORT_BASE_URL}/generate_publicity/`,
            method: 'post',
            data: {
                platform: data.platform,
                title: data.title,
                content: data.content,
                tags: data.tags,
                eventName: data.eventName,
                eventType: data.eventType,
                promotionTendency: data.promotionTendency,
                promotionMethod: data.promotionMethod
            }
        });
    }
}

export default ReportAPI;