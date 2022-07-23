import os
from dotenv import load_dotenv
load_dotenv()

from faker import Faker

from alpaca.broker.client import BrokerClient
from alpaca.broker.models import (
                        Contact,
                        Identity,
                        Disclosures,
                        Agreement
                    )
from alpaca.broker.models.requests import AccountCreationRequest
from alpaca.broker.enums import TaxIdType, FundingSource, AgreementType

BROKER_API_KEY = os.environ.get("APCA_BROKER_API_KEY")
BROKER_SECRET_KEY = os.environ.get("APCA_BROKER_API_SECRET")

broker_client = BrokerClient(
                api_key=BROKER_API_KEY,
                secret_key=BROKER_SECRET_KEY,
                sandbox=True,
                )

fake = Faker()
fake_profile = fake.profile()

contact_data = Contact(
            email_address=fake.email(),
            phone_number=fake.phone_number(),
            street_address=[fake.street_address()],
            city=fake.city(),
            state=fake.state_abbr(),
            postal_code=fake.postcode(),
            country=fake.country()
            )
# Identity
identity_data = Identity(
        given_name=fake.first_name(),
        middle_name=fake.first_name(),
        family_name=fake.last_name(),
        date_of_birth=str(fake.date_of_birth(minimum_age=21, maximum_age=81)),
        tax_id=fake.ssn(),
        tax_id_type=TaxIdType.USA_SSN,
        country_of_citizenship="USA",
        country_of_birth="USA",
        country_of_tax_residence="USA",
        funding_source=[FundingSource.EMPLOYMENT_INCOME]
        )

# Disclosures
disclosure_data = Disclosures(
        is_control_person=False,
        is_affiliated_exchange_or_finra=False,
        is_politically_exposed=False,
        immediate_family_exposed=False,
        )

# Agreements
agreement_data = [
    Agreement(
      agreement=AgreementType.MARGIN,
      signed_at="2020-09-11T18:09:33Z",
      ip_address="185.13.21.99",
    ),
    Agreement(
      agreement=AgreementType.ACCOUNT,
      signed_at="2020-09-11T18:13:44Z",
      ip_address="185.13.21.99",
    ),
    Agreement(
      agreement=AgreementType.CUSTOMER,
      signed_at="2020-09-11T18:13:44Z",
      ip_address="185.13.21.99",
    ),
    Agreement(
      agreement=AgreementType.CRYPTO,
      signed_at="2020-09-11T18:13:44Z",
      ip_address="185.13.21.99",
    )
]

# ## CreateAccountRequest ## #
account_data = AccountCreationRequest(
                        contact=contact_data,
                        identity=identity_data,
                        disclosures=disclosure_data,
                        agreements=agreement_data
                        )

# Make a request to create a new brokerage account
account = broker_client.create_account(account_data)

print(account)