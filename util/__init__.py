"""
Utility functions
"""
from .fast_ewma import ewma
from .fast_smooth import smooth, smooth_normal
from .multiprocess import expand_call, lin_parts, mp_pandas_obj, nested_parts, process_jobs, process_jobs_, \
    report_progress
from .utils import sample_df, get_daily_vol, convert_tz

from .metrics import log_returns
from .metrics import returns_gmean
from .metrics import pct_to_log_return
from .metrics import log_to_pct_return

from .metrics import sharpe_iid
from .metrics import sharpe_iid_adjusted
from .metrics import sharpe_iid_rolling
from .metrics import adjusted_sharpe

from .metrics import sharpe_autocorr_factor
from .metrics import sharpe_non_iid

from .metrics import LPM
from .metrics import kappa
from .metrics import kappa3
from .metrics import omega

from .metrics import sortino_iid
from .metrics import sortino

# can't have calmar ratio here yet as drawdown functions not present.
# from .metrics import calmar_ratio

from .metrics import tail_ratio

from .metrics import trading_days

from .metrics import annual_geometric_returns
from .metrics import annualized_pct_return
from .metrics import annualized_log_return

from .metrics import drawdown
from .metrics import calmar_ratio
from .metrics import drawdown_from_rtns
from .metrics import max_drawdown
from .metrics import max_drawdown_from_rtns
