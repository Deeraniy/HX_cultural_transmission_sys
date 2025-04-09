import request from "@/utils/request";

const DICT_BASE_URL = "";

class ThemeAPI {
    static getThemeCommentsSentiment() {
        return request({
            url: `${DICT_BASE_URL}/get_theme_comments_sentiment/`,
            method: "get",
        });
    }

    static getThemeIpDistribution() {
        return request({
            url: `${DICT_BASE_URL}/get_theme_ip_distribution/`,
            method: "get",
        });
    }

    static getThemePlatformDistribution() {
        return request({
            url: `${DICT_BASE_URL}/get_theme_platform_distribution/`,
            method: "get",
        });
    }

    static getThemeShortComments() {
        return request({
            url: `${DICT_BASE_URL}/get_theme_short_comments/`,
            method: "get",
        });
    }
}

export default ThemeAPI; 