function ClearStatistics( this )
%CLEARSTATISTICS Clears all Statistics

if this.m_holdStatistics
    this.m_rmseValues.ClearData();
    this.m_maeValues.ClearData();
    this.m_mbeValues.ClearData();
    this.m_stdErrValues.ClearData();
end

end

