from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Assignment, AssignmentSubmission
from courses.models import Course
from users.models import User
from django.contrib import messages

@login_required
def assignment_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    assignments = course.assignments.all()
    is_teacher = request.user.is_staff or request.user.is_superuser
    return render(request, 'assignments/assignment_list.html', {
        'course': course,
        'assignments': assignments,
        'is_teacher': is_teacher,
    })


@login_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submissions = assignment.submissions.select_related('student').all()
    is_teacher = request.user.is_staff or request.user.is_superuser
    # 学生提交作业
    if request.method == 'POST':
        if not is_teacher:
            if 'file' in request.FILES:
                AssignmentSubmission.objects.create(
                    assignment=assignment,
                    student=request.user,
                    file=request.FILES['file']
                )
                messages.success(request, '作业提交成功')
                return redirect('assignment_detail', assignment_id=assignment_id)
            else:
                messages.error(request, '请上传文件')
        else:
            # 教师批改作业
            grade_id = request.POST.get('grade_id')
            score = request.POST.get('score')
            comment = request.POST.get('comment')
            if grade_id:
                submission = AssignmentSubmission.objects.filter(id=grade_id, assignment=assignment).first()
                if submission:
                    submission.score = score if score != '' else None
                    submission.comment = comment
                    submission.save()
                    messages.success(request, '批改已保存')
                else:
                    messages.error(request, '未找到该提交记录')
                return redirect('assignment_detail', assignment_id=assignment_id)
    # 检查当前学生是否已提交
    user_submission = None
    if not is_teacher:
        user_submission = assignment.submissions.filter(student=request.user).first()
    return render(request, 'assignments/assignment_detail.html', {
        'assignment': assignment,
        'submissions': submissions,
        'is_teacher': is_teacher,
        'user_submission': user_submission,
    })

@login_required
def assignment_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, '无权限')
        return redirect('assignment_list', course_id=course_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        Assignment.objects.create(course=course, title=title, description=description, deadline=deadline)
        return redirect('assignment_list', course_id=course_id)
    return render(request, 'assignments/assignment_form.html', {'course': course})

@login_required
def assignment_update(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, '无权限')
        return redirect('assignment_detail', assignment_id=assignment_id)
    if request.method == 'POST':
        assignment.title = request.POST.get('title')
        assignment.description = request.POST.get('description')
        assignment.deadline = request.POST.get('deadline')
        assignment.save()
        return redirect('assignment_detail', assignment_id=assignment_id)
    return render(request, 'assignments/assignment_form.html', {'assignment': assignment})

@login_required
def assignment_delete(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    course_id = assignment.course.id
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, '无权限')
        return redirect('assignment_detail', assignment_id=assignment_id)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignment_list', course_id=course_id)
    return render(request, 'assignments/assignment_confirm_delete.html', {'assignment': assignment})
