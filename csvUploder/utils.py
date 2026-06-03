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



def get_difficulty_context(exam_type, problem_level):
    if exam_type == "practice" and problem_level == "beginner":
        difficulty_context = """
        Difficulty Profile: Beginner Practice

        Purpose:
        - Reinforce newly learned concepts
        - Build confidence through successful execution
        - Verify basic understanding

        Test Case Generation Rules:
        - Generate mostly normal test cases
        - Generate a few simple edge cases
        - Keep inputs small and readable
        - Use straightforward data patterns

        Edge Case Generation Rules:
        - Include only obvious boundary conditions
        - Include minimum valid inputs
        - Include maximum valid inputs only if still simple
        - Avoid tricky combinations

        Do Not Generate:
        - Stress tests
        - Adversarial tests
        - Hidden corner cases
        - Worst-case inputs
        - Performance-focused tests

        Complexity Requirements:
        - Ignore time complexity
        - Ignore memory complexity

        Coverage Expectations:
        - Basic correctness only
        - Happy-path scenarios
        - Common valid inputs

        Goal:
        - Ensure a student who understands the topic can pass comfortably
        """


    elif exam_type == "practice" and problem_level == "intermediate":
        difficulty_context = """
        Difficulty Profile: Intermediate Practice

        Purpose:
        - Strengthen conceptual understanding
        - Encourage handling of edge conditions
        - Identify common implementation mistakes

        Test Case Generation Rules:
        - Generate normal test cases
        - Generate edge cases
        - Generate simple corner cases
        - Mix easy and moderately challenging inputs

        Edge Case Generation Rules:
        - Include boundary values
        - Include duplicate values when applicable
        - Include unusual but valid inputs
        - Include special structures and patterns

        Do Not Generate:
        - Large stress tests
        - Highly adversarial inputs
        - Rare pathological cases

        Complexity Requirements:
        - Light complexity awareness allowed
        - Detect obviously inefficient approaches
        - Do not heavily penalize suboptimal solutions

        Coverage Expectations:
        - Normal cases
        - Edge cases
        - Common student mistakes
        - Boundary handling

        Goal:
        - Encourage robust solutions without making practice frustrating
        """


    elif exam_type == "practice" and problem_level == "advanced":
        difficulty_context = """
        Difficulty Profile: Advanced Practice

        Purpose:
        - Prepare students for challenging assessments
        - Encourage production-quality solutions
        - Expose hidden weaknesses

        Test Case Generation Rules:
        - Generate normal test cases
        - Generate edge cases
        - Generate corner cases
        - Generate moderate stress cases
        - Include tricky input patterns

        Edge Case Generation Rules:
        - Include all important boundaries
        - Include difficult combinations of constraints
        - Include uncommon but valid scenarios
        - Include cases that trigger common bugs

        Allow:
        - Moderate stress testing
        - Algorithmic validation
        - Complex input distributions
        - Hidden logical traps

        Avoid:
        - Excessive adversarial testing
        - Extremely large stress tests designed solely to fail solutions

        Complexity Requirements:
        - Check expected time complexity
        - Check expected memory complexity when relevant
        - Flag obviously inefficient approaches

        Coverage Expectations:
        - Broad coverage
        - Boundary coverage
        - Failure-mode coverage
        - Common bug detection

        Goal:
        - Prepare learners for advanced exams and competitive-style questions while remaining educational
        """

    elif exam_type == "midterm" and problem_level == "beginner":
        difficulty_context = """
        Difficulty Profile: Beginner Midterm

        Purpose:
        - Assess understanding of fundamental concepts
        - Verify correct implementation under typical conditions
        - Ensure basic boundary handling

        Test Case Generation Rules:
        - Generate normal test cases
        - Generate edge cases
        - Include basic corner cases
        - Use small to medium input sizes

        Edge Case Generation Rules:
        - Minimum valid inputs
        - Maximum valid inputs
        - Single-element cases
        - Empty structures when allowed
        - Basic boundary transitions

        Do Not Generate:
        - Large stress tests
        - Adversarial inputs
        - Pathological cases

        Complexity Requirements:
        - Light awareness of efficiency
        - Ignore advanced optimization concerns

        Coverage Expectations:
        - Normal scenarios
        - Boundary conditions
        - Common implementation mistakes

        Goal:
        - Distinguish prepared students from underprepared students
        - Focus primarily on correctness
        """

    elif exam_type == "midterm" and problem_level == "intermediate":
        difficulty_context = """
        Difficulty Profile: Intermediate Midterm

        Purpose:
        - Assess conceptual understanding
        - Evaluate robustness of implementation
        - Verify handling of uncommon valid inputs

        Test Case Generation Rules:
        - Generate normal test cases
        - Generate edge cases
        - Generate corner cases
        - Include moderately challenging inputs

        Edge Case Generation Rules:
        - Boundary values
        - Duplicate values
        - Sorted and reverse-sorted inputs
        - Sparse and dense patterns
        - Special structural configurations

        Allow:
        - Moderate input sizes
        - Tricky but fair scenarios
        - Cases targeting common logical mistakes

        Do Not Generate:
        - Full stress tests
        - Highly adversarial cases
        - Rare pathological constructions

        Complexity Requirements:
        - Check for reasonable efficiency
        - Detect obviously inefficient algorithms

        Coverage Expectations:
        - Normal cases
        - Edge cases
        - Corner cases
        - Common bug patterns

        Goal:
        - Differentiate average solutions from robust solutions
        """

    elif exam_type == "midterm" and problem_level == "advanced":
        difficulty_context = """
        Difficulty Profile: Advanced Midterm

        Purpose:
        - Evaluate deep understanding
        - Test algorithmic thinking
        - Expose weaknesses in implementation

        Test Case Generation Rules:
        - Generate normal test cases
        - Generate edge cases
        - Generate corner cases
        - Generate moderate stress tests

        Edge Case Generation Rules:
        - Extreme boundary values
        - Constraint interaction cases
        - Degenerate structures
        - Difficult but valid configurations
        - Hidden logical traps

        Allow:
        - Moderate stress testing
        - Performance-sensitive inputs
        - Cases targeting common advanced mistakes

        Avoid:
        - Extremely adversarial inputs
        - Maximum-scale stress tests intended for final exams

        Complexity Requirements:
        - Validate expected time complexity
        - Validate expected memory usage
        - Penalize clearly inefficient approaches

        Coverage Expectations:
        - Broad coverage
        - Boundary coverage
        - Logic coverage
        - Performance awareness

        Goal:
        - Separate strong students from exceptional students
        - Reward both correctness and efficiency
        """


    elif exam_type == "endterm" and problem_level == "beginner":
        difficulty_context = """
        Difficulty Profile: Beginner Endterm

        Purpose:
        - Verify complete understanding of fundamental concepts
        - Ensure solutions handle all standard scenarios
        - Evaluate readiness for progression to higher-level topics

        Test Case Generation Rules:
        - Generate normal test cases
        - Generate edge cases
        - Generate corner cases
        - Include a few small stress cases

        Edge Case Generation Rules:
        - Minimum valid inputs
        - Maximum valid inputs
        - Single-element cases
        - Empty structures when allowed
        - Boundary transitions
        - Common special cases

        Allow:
        - Moderate input sizes
        - Cases targeting common mistakes
        - Basic performance checks

        Do Not Generate:
        - Highly adversarial inputs
        - Pathological worst-case constructions

        Complexity Requirements:
        - Verify reasonable efficiency
        - Reject obviously inefficient approaches

        Coverage Expectations:
        - Normal cases
        - Edge cases
        - Corner cases
        - Common implementation bugs

        Goal:
        - Ensure students can produce reliable solutions for all standard scenarios
        """


    elif exam_type == "endterm" and problem_level == "intermediate":
        difficulty_context = """
        Difficulty Profile: Intermediate Endterm

        Purpose:
        - Evaluate correctness, robustness, and efficiency
        - Ensure solutions work under diverse conditions
        - Test algorithmic understanding beyond basic implementation

        Test Case Generation Rules:
        - Generate normal test cases
        - Generate edge cases
        - Generate corner cases
        - Generate stress tests

        Edge Case Generation Rules:
        - Extreme boundary values
        - Constraint interaction cases
        - Duplicate-heavy inputs
        - Degenerate structures
        - Special distributions
        - Difficult but valid configurations

        Allow:
        - Large input sizes
        - Performance-sensitive inputs
        - Cases exposing common logical mistakes

        Generate Stress Tests:
        - Maximum or near-maximum constraints
        - Large random inputs
        - Large structured inputs

        Complexity Requirements:
        - Validate expected time complexity
        - Validate expected memory complexity
        - Detect inefficient algorithms

        Coverage Expectations:
        - Broad correctness coverage
        - Boundary coverage
        - Logic coverage
        - Performance coverage

        Goal:
        - Differentiate competent solutions from highly robust solutions
        """


    elif exam_type == "endterm" and problem_level == "advanced":
        difficulty_context = """
        Difficulty Profile: Advanced Endterm

        Purpose:
        - Perform exhaustive evaluation of solution quality
        - Verify correctness under all significant scenarios
        - Distinguish optimal solutions from merely correct solutions

        Test Case Generation Rules:
        - Generate normal test cases
        - Generate edge cases
        - Generate corner cases
        - Generate stress tests
        - Generate adversarial tests

        Edge Case Generation Rules:
        - Minimum and maximum boundaries
        - Multiple interacting boundaries
        - Degenerate structures
        - Rare but valid configurations
        - Constraint interaction failures
        - Hidden logical traps

        Generate Stress Tests:
        - Maximum constraint inputs
        - Large randomized inputs
        - Large structured inputs
        - Worst-case distributions

        Generate Adversarial Tests:
        - Inputs targeting common bugs
        - Inputs targeting inefficient algorithms
        - Inputs targeting incorrect assumptions
        - Inputs exposing off-by-one errors
        - Inputs exposing indexing errors
        - Inputs exposing overflow issues
        - Inputs exposing recursion-depth problems

        Complexity Requirements:
        - Strict time complexity validation
        - Strict memory complexity validation
        - Reject non-scalable solutions

        Coverage Expectations:
        - Full correctness coverage
        - Full boundary coverage
        - Full branch coverage
        - Failure-mode coverage
        - Performance coverage

        Bug Detection Focus:
        - Off-by-one errors
        - Overflow and underflow
        - Incorrect initialization
        - Invalid state transitions
        - Duplicate handling
        - Empty input handling
        - Precision issues
        - Data structure misuse

        Goal:
        - Separate top-performing students from all others
        - Require both correctness and algorithmic excellence
        """

    else:
        difficulty_context = """
        Difficulty Profile: Standard
        - Generate normal and edge test cases
        - Basic correctness coverage
        - No stress tests
        """

    return difficulty_context