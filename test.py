# import xmlrpc.client
#
url = "http://test.nurasolar.uic-erp.uz"
db = "test"
username = "admin"
password = "admin"

# # Auth
# common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
# uid = common.authenticate(db, username, password, {})
#
# models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
#
# partners = models.execute_kw(
#     db, uid, password,
#     'account.move', 'search_read',
#     [[['partner_id', '=', 292], ['move_type', 'in', ['out_invoice', 'out_refund']]], ['name', 'amount_total']],   # [] → hamma yozuvlar, fields → kerakli ustunlar
#     {'limit': 50}                       # limit qo'ymasangiz, juda katta ro'yxat qaytishi mumkin
# )
#
# amount_total = 0
# for partner in partners:
#     amount_total += partner['amount_total']
#     print(f"ID: {partner['id']}, Name: {partner['name']}")
#
# print(amount_total)
# print("UID:", uid)
#
#
import xmlrpc.client
# from test import db, url, username, password

# Odoo'ga ulanish
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

if not uid:
    print("❌ Login xato! Username yoki parol noto‘g‘ri.")
else:
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    # Telefon raqam
    phone_number = "+998991259009"

    # Faqat raqamlarni tozalash (bo‘shliq, + belgilarini olib tashlash)
    clean_number = phone_number.replace(" ", "").replace("+", "").replace("-", "").replace("(", "").replace(")", "")

    # Qidirish (phone va mobile maydonlarida qisman)
    partners = models.execute_kw(
        db, uid, password,
        'res.partner', 'search_read',
        [[
            '|',
            ['phone', 'ilike', clean_number],
            ['mobile', 'ilike', clean_number]
        ]],
        {'fields': ['id', 'name', 'phone', 'mobile'], 'limit': 5}
    )

    if partners:
        print("✅ Topildi:", partners)
    else:
        print("❌ Telefon raqam topilmadi")
