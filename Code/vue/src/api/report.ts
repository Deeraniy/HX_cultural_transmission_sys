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
        // 生成英文宣传报告
        static generatePublicityENReportAPI(data: {
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
                url: `${REPORT_BASE_URL}/generate_publicity_en/`,
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

    // 生成宣传图片
    static generatePublicityImageAPI(data: {
        eventName: string;
        eventType: string;
        tags?: string[];
        title?: string;
        content?: string;
    }) {
        return request({
            url: `${REPORT_BASE_URL}/api/report/generate_image/`,
            method: 'post',
            data
        });
    }

    // 生成英文宣传图片
    static generatePublicityImageENAPI(data: {
        eventName: string;
        eventType: string;
        tags?: string[];
        title?: string;
        content?: string;
        }) {
            return request({
                url: `${REPORT_BASE_URL}/api/report/generate_image_en/`,
                method: 'post',
                data
            });
        }
}

export default ReportAPI;
