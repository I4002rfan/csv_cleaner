from .models import Course



def get_coverage(course_id, module_tags):
    
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return None
    
    module = course.syllabus['modules']
    module_names = [m['name'] for m in module]
    if not module_names:
        return None

    latest_postion = 0
    for tag in module_tags:
        for i, name in enumerate(module_names):
            if tag.lower() == name.lower():
                if i > latest_postion:
                    latest_postion = i

    if latest_postion == 0 and not any(tag.lower() == module_names[0].lower() for tag in module_tags):
        return None

    topic_covered = module_names[:latest_postion + 1]
    topic_not_covered = module_names[latest_postion + 1:]     

    return {
    'topics_covered': topic_covered,
    'topics_not_covered': topic_not_covered,
    'focus_topics': module_tags
}