import datetime
import os
from travel_recommend import settings

class UploadAvatar(APIView):
    def post(self, request):
        file = request.FILES.get('avatar')
        if not file:
            return response.server_error(message="上传文件不能为空")
        new_file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '-' + file.name
        file_path = os.path.join(settings.USER_AVATAR_ROOT, new_file_name)
        try:
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            return response.success_data_msg(f'{settings.USER_MEDIA_URL}' + new_file_name, "上传成功")
        except:
            return response.server_error("上传头像失败")
