import random
import string


def random_string():
	return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(20)])


def _filename(instance, filename, _prefix):
	_post_fix = random_string()
	file_name = filename.lower().split('.')[0][:5]
	file_extension = filename.split('.')[-1]

	return '%s/%s.%s.%s' % (_prefix, file_name, _post_fix, file_extension)


def user_avatar_dir(instance, filename):
	return 'user/' + _filename(instance, filename, r'avatar')


def official_id_dir(instance, filename):
	return 'user/' + _filename(instance, filename, r'official_id')


def investor_doc_dir(instance, filename):
	return 'user/' + _filename(instance, filename, r'investor_doc')


def company_icon_dir(instance, filename):
	return 'company/' + _filename(instance, filename, r'icon')


def company_member_avatar_dir(instance, filename):
	return 'company/' + _filename(instance, filename, r'member_avatars')
