company_filter = (
    'department_id',
    'company_id',
    'number',
    'name'
)

work_hours_filter = (
    'id',
    'department_id',
    'company_id',
    'name',
    'number',
    'm_start_time',
    'm_end_time',
    'a_start_time',
    'a_end_time',
    'single_week_hours',
    'double_week_hours',
    'month_hours',
    'overtime_initial_value',
)

salary_sum_filter = (
    'id',
    'year',
    'month',
    'actual_salary',
    'submited',
    'verified',
    'post',
    'payed_mode',
)


m_pieces_sum_filter = (
    'username',
    'date',
    'id',
    'year',
    'month',
    'submited',
    'verified',
)

attendance_sum_filter = (
    'username',
    'date',
    'id',
    'year',
    'month',
    'submited',
    'verified'
)

user_info_all_filter = (
    'user_info_id',
    'phone_num',
    'number',
    'base_salary',
    # 'bank',
    'username',
    'department',
    'role_id',
    'role_name',
    'company_name',
)

user_info_birthday_filter = (
    'user_info_id',
    'phone_num',
    # 'bank',
    'birthday',
    'username',
    'company_name',
)

attendance_filter = (
    'username',
    'date',
    'attendance_id',
    'year',
    'month',
    'submited',
    'verified'
)

salary_filter = (
    'username',
    'salary_id',
    'year',
    'month',
    'actual_salary',
    'submited',
    'verified',
    'post',
    'payed_mode',
)

m_hours_filter = (
    'm_hours_id',
    'year',
    'month',
    'submited',
    'verified',
)

m_pieces_filter = (
    'username',
    'date',
    'm_pieces_id',
    'year',
    'month',
    'submited',
    'verified',
)

vacation_appl_filter = (
    'username',
    'vacation_appl_id',
    'create_time',
    'vacation_type',
    'submited',
    'verified',
    'reason'
)

overtime_appl_filter = (
    'overtime_appl_id',
    'create_time',
    'department',
    'reason',
    'submited',
    'verified',
    'username',
)

app_appl_filter = (
    'app_appl_id',
    'username',
    'degree',
    'phone_num',
    'date',
)

acc_appl_filter = (
    'acc_appl_id',
    'username',
    'payed_mode',
    'post',
    'date',
)

add_appl_filter = (
    'acc_appl_id',
    'username',
    'payed_mode',
    'post',
    'date',
)

zz_appl_filter = (
    'zz_appl_id',
    'username',
    'attr',
    'post',
    'date',
    'submited',
    'verified',
    'entry_end_date'
)

dep_appl_filter = (
    'dep_appl_id',
    'username',
    'post',
    'date',
    'type',
)

reward_appl_filter = (
    'reward_appl_id',
    'username',
    'date',
    'reason',
    'verified',
    'submited',
)

terlabor_appl_filter = (
    'terlabor_appl_id',
    'username',
    'post',
    'dep_date',
    'date',
    'labor_end_date',
    'attr',
    'submited',
    'verified',
)

contract_filter = (
    'contract_id',
    'year',
    'month',
    'submited',
    'verified'
)

manager_contract_filter = (
    'contract_id',
    'username',
    'payed_mode',
    'post',
    'date',
)

# todo : 这里的verify是员工有没有审核,非该申请本身
gs_overtime_appl_filter = (
    'gs_overtime_appl_id',
    'username',
    'department',
    'reason',
    'create_time',
    'verified'
)


# todo : 这里的verify是员工有没有审核,非该申请本身
gs_vacation_appl_filter = (
    'gs_vacation_appl_id',
    'username',
    'department',
    'reason',
    'create_time',
    'verified'
)

post_adjust_appl_filter = (
    'paa_id',
    'username',
    'post',
    'to_post',
    'date',
    'submited',
    'verified',
    'reason',
)

warn_appl_filter = (
    'warn_appl_id',
    'username',
    'date',
    'reason',
    'submited',
    'verified'
)

salary_adjust_appl_filter = (
    'saa_id',
    'username',
    'base_salary',
    'to_base_salary',
    'date',
    'submited',
    'verified',
    'post',
    'payed_mode',
)

law_filter = (
    'law_id',
    'q',
)

def get_apply_filter(tp):
    apply_filter = ''
    if tp=='zz':
        apply_filter = zz_appl_filter
    elif tp=='app':
        apply_filter = app_appl_filter
    elif tp=='acc':
        apply_filter = acc_appl_filter
    elif tp=='add':
        apply_filter = add_appl_filter
    elif tp=='dep':
        apply_filter = dep_appl_filter
    elif tp=='post_adjust':
        apply_filter = post_adjust_appl_filter
    elif tp=='gs_overtime':
        apply_filter = gs_overtime_appl_filter
    elif tp=='gs_vacation':
        apply_filter = gs_vacation_appl_filter
    elif tp=='reward':
        apply_filter = reward_appl_filter
    elif tp=='terlabor':
        apply_filter = terlabor_appl_filter
    elif tp=='warn':
        apply_filter = warn_appl_filter
    elif tp=='salary_adjust':
        apply_filter = salary_adjust_appl_filter
    elif tp == 'vacation':
        apply_filter = vacation_appl_filter
    elif tp == 'overtime':
        apply_filter = overtime_appl_filter
    elif tp=='attendance':
        apply_filter = attendance_filter
    elif tp=='m_hours':
        apply_filter = m_hours_filter
    elif tp=='salary':
        apply_filter = salary_filter
    elif tp=='m_pieces':
        apply_filter = m_pieces_filter
    elif tp=='m_pieces_sum':
        apply_filter = m_pieces_sum_filter
    elif tp=='salary_sum':
        apply_filter = salary_sum_filter
    elif tp=='attendance_sum':
        apply_filter = attendance_sum_filter
    elif tp=='contract':
        apply_filter = contract_filter
    elif tp=='manager_contract':
        apply_filter = manager_contract_filter
    elif tp=='law':
        apply_filter = law_filter

    elif tp=='company':
        apply_filter = company_filter
    elif tp=='work_hours':
        apply_filter = work_hours_filter
    return apply_filter

