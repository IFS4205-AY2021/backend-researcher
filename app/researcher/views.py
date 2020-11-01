from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.decorators import csrf
from django.http import HttpResponse
from .models import UserInfo, Researcher, Contact, K_User

given_k = 2
# Create your views here.
def home(request):
    return render(request, 'home.html', {})


def dashboard(request):
    return render(request, 'dashboard.html', {})


def message_display_home(request, message):
    return render(request, 'message_display_home.html', context={'data': message})


def message_display_dashboard(request, message):
    return render(request, 'message_display_dashboard.html', context={'data': message})


def registration(request):
    if request.POST:
        return render(request, 'register.html')

    return HttpResponse("Invalid request")


def register(request):
    if request.POST:
        name = request.POST['username']
        phone_no = request.POST['phone']
        pw = request.POST['pw']

        user = Researcher.objects.filter(phone=phone_no)

        if user.exists():
            message = "User already exists. Please go back to Home page."
            return message_display_home(request, message)
        else:
            Researcher.objects.create(name=name, phone=phone_no, encryption_keys=pw)

            message = "Register successfully. Please go back to Home page"
            return message_display_home(request, message)

    else:
        return HttpResponse("Invalid request")


def login(request):
    if request.POST:
        phone = request.POST['phone']
        pw = request.POST['pw']

        user = Researcher.objects.get(phone=phone)
        if pw == user.encryption_keys:
            return render(request, 'dashboard.html', context={'data': list_cluster(request)})

    return HttpResponse("Invalid request")


def list(request):
    if request.POST:
        age_min = request.POST['Age_minimal']
        age_max = request.POST['Age_maximal']
        location = request.POST['location']
        gender = request.POST['gender']
        test_result = request.POST['test_result']
        cluster_id = request.POST['cluster_id']
        print("cluster:")
        print(cluster_id)
        if cluster_id != "":
            return list_clu(request, cluster_id)
        elif age_max == "" and age_min == "" and location == "" and gender == "" and test_result == "":
            return list_all(request)
        elif (age_max != "" or age_min != "") and location == "" and gender == "" and test_result == "":
            return list_age(request, age_min, age_max, UserInfo.objects.all())
        elif (age_max != "" or age_min != "") and location != "" and gender == "" and test_result == "":
            return list_age(request, age_min, age_max, UserInfo.objects.filter(location=location))
        elif (age_max != "" or age_min != "") and location == "" and gender != "" and test_result == "":
            return list_age(request, age_min, age_max, UserInfo.objects.filter(gender=gender))
        elif (age_max != "" or age_min != "") and location == "" and gender == "" and test_result != "":
            return list_age(request, age_min, age_max, UserInfo.objects.filter(test_result=test_result))
        elif (age_max != "" or age_min != "") and location != "" and gender != "" and test_result == "":
            return list_age(request, age_min, age_max, UserInfo.objects.filter(location=location).filter(gender=gender))
        elif (age_max != "" or age_min != "") and location != "" and gender == "" and test_result != "":
            return list_age(request, age_min, age_max, UserInfo.objects.filter(location=location).filter(test_result=test_result))
        elif (age_max != "" or age_min != "") and location == "" and gender != "" and test_result != "":
            return list_age(request, age_min, age_max, UserInfo.objects.filter(test_result=test_result).filter(gender=gender))
        elif (age_max != "" or age_min != "") and location != "" and gender != "" and test_result != "":
            return list_age(request, age_min, age_max, UserInfo.objects.filter(location=location).filter(gender=gender).filter(test_result=test_result))
        elif age_max == "" and age_min == "" and location != "" and gender == "" and test_result == "":
            return list_loc(request, location, UserInfo.objects.all())
        elif age_max == "" and age_min == "" and location != "" and gender == "" and test_result != "":
            return list_loc(request, location, UserInfo.objects.filter(test_result=test_result))
        elif age_max == "" and age_min == "" and location != "" and gender != "" and test_result == "":
            return list_loc(request, location, UserInfo.objects.filter(gender=gender))
        elif age_max == "" and age_min == "" and location != "" and gender != "" and test_result != "":
            return list_loc(request, location, UserInfo.objects.filter(test_result=test_result).filter(gender=gender))
        elif age_max == "" and age_min == "" and location == "" and gender != "" and test_result == "":
            return list_gen(request, gender, UserInfo.objects.all())
        elif age_max == "" and age_min == "" and location == "" and gender == "" and test_result != "":
            return list_res(request, test_result, UserInfo.objects.all())
        elif age_max == "" and age_min == "" and location != "" and gender != "" and test_result != "":
            return list_gen(request, gender, UserInfo.objects.filter(test_result=test_result))
        else:
            return HttpResponse("Invalid request")

    return HttpResponse("Invalid request")


def list_all(request):
    persons = k_anonymity(request, UserInfo.objects.all())
    return export_csv(request, persons)


def list_clu(request, cluster_id):
    user_list = UserInfo.objects.filter(cluster_id=cluster_id)
    users = k_anonymity(request, user_list)
    total_num = count_total(request, cluster_id)
    total_infected_num = count_total_infected(request, cluster_id)
    per = total_infected_num/total_num * 100
    total_F = user_list.filter(gender="F").count()
    total_M = user_list.filter(gender="M").count()
    return render(request, 'cluster.html', context={'id': cluster_id, 'data': users, 'total_num': total_num,
                                                    'total_infected_num': total_infected_num, 'per': per,
                                                    'total_F': total_F, 'total_M': total_M})


def list_age(request, age_min, age_max, user_list):
    if age_min == "":
        persons = k_anonymity(request, user_list.filter(age__lte=age_max))
        return export_csv(request, persons)
    elif age_max == "":
        persons = k_anonymity(request, user_list.filter(age__gte=age_min))
        return export_csv(request, persons)
    else:
        filtered_users = user_list.filter(age__lte=age_max)
        persons = k_anonymity(request, filtered_users.filter(age__gte=age_min))
        return export_csv(request, persons)


def list_loc(request, location, user_list):
    persons = k_anonymity(request, user_list.filter(location=location))
    return export_csv(request, persons)


def list_res(request, test_result, user_list):
    persons = k_anonymity(request, user_list.filter(test_result=test_result))
    return export_csv(request, persons)


def list_gen(request, gender, user_list):
    persons = k_anonymity(request, user_list.filter(gender=gender))
    return export_csv(request, persons)


def read_csv(users):
    persons = []
    for p in users:
        u = K_User.objects.create(age=p.age, age_min=p.age, age_max=p.age, gender=p.gender, location=p.location,
                                  test_result=p.test_result,
                                  cluster_id=p.cluster_id
                                  )
        persons.append(u)
    return persons


def anonymize_age(persons, times):
    for p in persons:
        age_range = 5 * times
        # if times == 1:
        #     p.age = int(p.age/5)*5
        # elif times == 2:
        #     p.age = int(p.age/10)*10
        # elif times > 2:
        p.age_min = int(p.age / age_range) * age_range
        p.age_max = p.age_min + age_range
    return persons  # 返回列表型


def anonymize_loc(persons, times):
    for p in persons:
        val = times * (-1)
        p.location = p.location[:val] + "*" * times
        print(p.location)
    return persons  # 返回列表型


def anonymize_gender(persons):  # 泛化
    for p in persons:
        p.gender = '*'
    return persons  # 返回列表型


# def copy_persons(fresh_persons):  # 拷贝数据列表
#     persons = []
#     for p in fresh_persons:
#         u = UserInfo.objects.create(name=p.name, phone=p.phone, age=p.age, address=p.address, location=p.location,
#                                 test_result=p.test_result, encryption_keys=p.encryption_keys, personal_id=p.personal_id)
#         persons.append(u)
#     return persons


def group_persons(persons):  # 将数据分组，具体原理参考get_num
    grouped_persons = {}
    for p in persons:
        pseudo_parameters = str(p.age_min) + str(p.age_max) + str(p.location) + str(p.gender)
        if grouped_persons.get(pseudo_parameters) is None:
            grouped_persons[pseudo_parameters] = []
        grouped_persons[pseudo_parameters].append(p)
    print(grouped_persons)
    return grouped_persons  # 返回字典型，每个组以键值对的形式存储


def get_k(grouped_persons):  # 获得k值（传入字典型泛化结果）
    tmpDict = {}
    for group in grouped_persons:  # 遍历所有键值对
        tmpDict[group] = len(grouped_persons[group])  # 获得每个键对应值的个数
        # 即每个分组的包含的person个数
        # 以键(组标识)值(person个数)对存在字典tmpDict里
    k = None
    for group in tmpDict:  # 遍历tmpDict，取出最小的person个数，赋值给k
        if k is None or tmpDict[group] < k:
            k = tmpDict[group]
    return k  # 返回的k值即为泛化结果的k值


def export_csv(request, persons):

    return render(request, "list_all.html", context={"data": persons})


def get_num(persons, type):  # 获得数据某属性个数（具体属性由type决定）
    get_num_ = {}  # 一个字典（保存键值对）
    for p in persons:  # 遍历数据
        if type == 1:  # 年龄
            tmp_str = str(p.age_min) + str(p.age_max)  # 将某一个人的出生日期作为键tmp_str
        elif type == 2:  # 邮编
            tmp_str = str(p.location)  # 将某一个人的邮编作为键tmp_str
        elif type == 3:  # 性别
            tmp_str = str(p.gender)  # 将某一个人的邮编作为键tmp_str
        if get_num_.get(tmp_str) is None:  # 如果字典中没有此键
            get_num_[tmp_str] = []  # 增加以tmp_str为键，值为空的键值对
        get_num_[tmp_str].append(p)  # 将此人的数据加到tmp_str键所对的值中
    tmp_str = {}
    return len(get_num_)  # 返回了字典中键的个数（就是属性个数）


def max_num(age_num, loc_num, gender_num):
    if age_num >= loc_num and age_num >= gender_num:
        return 1
    elif loc_num >= age_num and loc_num >= gender_num:
        return 2
    elif gender_num >= age_num and gender_num >= loc_num:
        return 3


def k_anonymity(request, user_list):
    satisfying_combinations = []
    persons = read_csv(user_list)
    age_times = 0
    loc_times = 0
    i = 0
    K_User.objects.all().delete()
    # persons = copy_persons(fresh_persons)
    while True:
        i = i + 1
        if i > 1000:
            print(i)
            break;
        grouped_persons = group_persons(persons)
        k = get_k(grouped_persons)
        print("get_K=" + str(k))
        if k >= given_k:
            satisfying_combinations.append(grouped_persons)
            break
        age_num = get_num(persons, 1)
        print("age_num=" + str(age_num))
        loc_num = get_num(persons, 2)
        print("loc_num=" + str(loc_num))
        gender_num = get_num(persons, 3)
        print("gen_num=" + str(gender_num))
        if age_num == 1 and loc_num == 1 and gender_num == 1:
            break
        m = max_num(age_num, loc_num, gender_num)
        if m == 1:
            age_times = age_times + 1
            print("age_times=" + str(age_times))
            persons = anonymize_age(persons, age_times)
        elif m == 2:
            loc_times = loc_times + 1
            print("any_loc")
            persons = anonymize_loc(persons, loc_times)
        elif m == 3:
            print("any_gen")
            persons = anonymize_gender(persons)

    if len(satisfying_combinations) > 0:
        return persons
    else:
        return HttpResponse("Failed.")


def list_cluster(request):
    users = UserInfo.objects.all()
    ids = []
    valid_ids = []
    for user in users:
        print(user.cluster_id)

        if user.cluster_id in ids:
            print("already exist")
            break
        else:
            ids.append(user.cluster_id)
            count = UserInfo.objects.filter(cluster_id=user.cluster_id).count()
            if count >= given_k:
                print("added")
                valid_ids.append(user.cluster_id)
    return valid_ids




def count_avg(request):
    if request.POST:
        location = request.POST['location']
        total_contact = 0
        person_no = 0
        data = UserInfo.objects.filter(location=location)
        for user in data:
            person_no = person_no + 1
            id = user.phone
            contact_data = Contact.objects.all()
            for contact in contact_data:
                if contact.person1_id == id or contact.person2_id == id:
                    total_contact = total_contact + 1
                    print(total_contact)

        if person_no == 0:
            return HttpResponse("Invalid location")

        else:
            avg = total_contact / person_no
            message = "The average number of contacts of all people living near " + str(location) + " is " + str(avg)
            return message_display_dashboard(request, message)

    else:
        return HttpResponse("Invalid request")


def count_avg_P(request):
    if request.POST:
        location = request.POST['location']
        total_contact = 0
        person_no = 0
        data = UserInfo.objects.filter(location=location)
        for user in data:
            person_no = person_no + 1
            id = user.phone
            contact_data = Contact.objects.all()
            for contact in contact_data:
                if contact.person1_id == id or contact.person2_id == id:
                    total_contact = total_contact + 1
                    print(total_contact)

        if person_no == 0:
            return HttpResponse("Invalid location")

        else:
            avg = total_contact / person_no
            message = "The average number of contacts of all people living near " + str(location) + " is " + str(avg)
            return message_display_dashboard(request, message)

    else:
        return HttpResponse("Invalid request")



def count_total(request, cluster_id):
    if request.POST:
        num = len(UserInfo.objects.filter(cluster_id=cluster_id))
        return num
    else:
        return HttpResponse("Invalid request")


def count_total_infected(request, cluster_id):
    if request.POST:
        num = len(UserInfo.objects.filter(cluster_id=cluster_id).filter(test_result="POSITIVE"))
        return num
    else:
        return HttpResponse("Invalid request")

def add_user_page(request):
    if request.POST:
        return add_user(request)

    else:
        return HttpResponse("Invalid request")


def add_user(request):
    if request.POST:
        name = str(request.POST['name'])
        phone_no = str(request.POST['phone'])
        address = request.POST['address']
        gender = request.POST['gender']
        location = str(request.POST['location'])
        age = int(request.POST['age'])
        test_result = str(request.POST['test_result'])
        pw = request.POST['pw']

        UserInfo.objects.create(name=name, phone=phone_no, age=age, gender=gender, address=address, location=location,
                            test_result=test_result, encryption_keys=pw)
        return message_display_dashboard(request, "User has been added")

    else:
        return HttpResponse("Invalid request")


def count_total_P(request):
    if request.POST:
        location = str(request.POST['location'])
        user_list = UserInfo.objects.filter(location=location)
        P_num = user_list.filter(test_result="POSITIVE").count()
        num = user_list.count()
        per = P_num / num * 100
        line1 = "The total number of people who has a POSITIVE test result is " + str(P_num) + ". "
        line2 = "And the percentage is " + str(per) + "%"
        lines = [line1, line2]
        response_content = '\r\n'.join(lines)
        return message_display_dashboard(request, response_content)
        # return HttpResponse(response_content, content_type="text/plain")
    else:
        return HttpResponse("Invalid request")
