import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="diycu6vqm",
    api_key="837721287245126",
    api_secret="6Oo8UQM65m5J2OKuLEXj920YOSI"
)

# رفع صورة للاختبار
response = cloudinary.uploader.upload("/home/ahmed/apps/green_carts_api/images/81o-hUhRCqL_f97wX5Z._AC_SL1500_.jpg")
print(response["url"])  # تحقق من الرابط الذي يتم إرجاعه
