from graphene import Field, Int, List, ObjectType, String


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        return root.jobs

    # @staticmethod
    # def resolve_jobs(root, info):
    #     return [job for job in jobs_data if job['employer_id'] == root['id']]


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)

    @staticmethod
    def resolve_employer(root, info):
        return root.employer

    # @staticmethod
    # def resolve_employer(root, info):
    #     return next(
    #         employer
    #         for employer in employers_data
    #         if employer['id'] == root['employer_id']
    #     )
